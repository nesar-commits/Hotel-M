"""Lightweight content-based recommendation engine.

Builds TF-IDF vectors from each menu item's name, description, cuisine tags
and category, then uses cosine similarity to power two features:

- "similar items" (item-to-item, e.g. "You might also like" on a dish page)
- "recommended for you" (builds a taste profile from a user's past orders and
  ranks all other items against it)

For cold-start users (no order history) we fall back to a popularity score
(rating-weighted).

This runs in-memory on each request since catalog sizes for a menu app are
small (hundreds to low thousands of items) — no need for an offline
training job or persisted model for the MVP.
"""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app import models


def _item_text(item: models.MenuItem) -> str:
    category_name = item.category.name if item.category else ""
    veg_tag = "vegetarian" if item.is_veg else "non-vegetarian"
    return " ".join(
        filter(
            None,
            [item.name, item.description, item.tags, category_name, veg_tag],
        )
    )


def _vectorize(items: list[models.MenuItem]):
    corpus = [_item_text(item) for item in items]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus)
    return matrix


def popular_items(items: list[models.MenuItem], top_n: int = 10) -> list[models.MenuItem]:
    ranked = sorted(items, key=lambda i: i.rating, reverse=True)
    return ranked[:top_n]


def similar_items(
    target_id: int, items: list[models.MenuItem], top_n: int = 6
) -> list[models.MenuItem]:
    if len(items) < 2:
        return []

    ids = [item.id for item in items]
    if target_id not in ids:
        return []

    matrix = _vectorize(items)
    target_idx = ids.index(target_id)
    similarities = cosine_similarity(matrix[target_idx], matrix).flatten()

    ranked_idx = similarities.argsort()[::-1]
    results = []
    for idx in ranked_idx:
        if idx == target_idx:
            continue
        results.append(items[idx])
        if len(results) >= top_n:
            break
    return results


def recommend_for_user(
    history_items: list[models.MenuItem],
    catalog_items: list[models.MenuItem],
    top_n: int = 10,
) -> list[models.MenuItem]:
    if not history_items:
        return popular_items(catalog_items, top_n)

    history_ids = {item.id for item in history_items}
    candidates = [item for item in catalog_items if item.id not in history_ids]
    if not candidates:
        return []

    # Build one combined "taste profile" document from everything the user
    # has ordered, and rank candidates against it.
    all_items = history_items + candidates
    matrix = _vectorize(all_items)

    profile_vector = matrix[: len(history_items)].mean(axis=0)
    candidate_matrix = matrix[len(history_items):]

    import numpy as np

    profile_vector = np.asarray(profile_vector)
    similarities = cosine_similarity(profile_vector, candidate_matrix).flatten()

    ranked_idx = similarities.argsort()[::-1][:top_n]
    return [candidates[idx] for idx in ranked_idx if similarities[idx] > 0] or popular_items(
        candidates, top_n
    )
