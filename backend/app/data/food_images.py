"""A pool of hand-verified, working Unsplash restaurant/hotel photo IDs.

Used exclusively for restaurant *cover* photos (`Restaurant.image_url`) —
actual dining rooms, hotel rooms, bars, cafes, resort pools, and building
exteriors, never food close-ups. Individual dish photos (used for menu
items) live separately in `bulk_restaurants.py`'s cuisine profiles and are
unaffected by this file.

Each ID here was checked (HTTP 200, real image bytes, then visually reviewed
in a contact sheet) before being added — candidates that were food/ingredient
close-ups, abstract shots, or unrelated subjects were dropped even when the
URL itself was valid, since the goal here is specifically "this looks like a
real place you could walk into," not "this looks like food."

True per-restaurant image uniqueness at scale (5,000+) isn't achievable
without a paid image API — this pool (45 photos) is used as a shared,
randomly-assigned resource with an even-spread algorithm, which keeps
repetition rare rather than eliminating it entirely.
"""

HERO_IMAGES = [
    "photo-1414235077428-338989a2e8c0",
    "photo-1439130490301-25e322d88054",
    "photo-1445019980597-93fa8acb246c",
    "photo-1445116572660-236099ec97a0",
    "photo-1449158743715-0a90ebb6d2d8",
    "photo-1481833761820-0509d3217039",
    "photo-1493857671505-72967e2e2760",
    "photo-1497935586351-b67a49e012bf",
    "photo-1512918728675-ed5a9ecdebfd",
    "photo-1517248135467-4c7edcad34c4",
    "photo-1519167758481-83f550bb49b3",
    "photo-1519690889869-e705e59f72e1",
    "photo-1519974719765-e6559eac2575",
    "photo-1521017432531-fbd92d768814",
    "photo-1521737711867-e3b97375f902",
    "photo-1522708323590-d24dbb6b0267",
    "photo-1524758631624-e2822e304c36",
    "photo-1533779283484-8ad4940aa3a8",
    "photo-1537047902294-62a40c20a6ae",
    "photo-1543007630-9710e4a00a20",
    "photo-1544148103-0773bf10d330",
    "photo-1546622891-02c72c1537b6",
    "photo-1550966871-3ed3cdb5ed0c",
    "photo-1552566626-52f8b828add9",
    "photo-1554118811-1e0d58224f24",
    "photo-1559339352-11d035aa65de",
    "photo-1560053608-13721e0d69e8",
    "photo-1560448204-e02f11c3d0e2",
    "photo-1560624052-449f5ddf0c31",
    "photo-1562778612-e1e0cda9915c",
    "photo-1565895405227-31cffbe0cf86",
    "photo-1568084680786-a84f91d1153c",
    "photo-1571003123894-1f0594d2b5d9",
    "photo-1571896349842-33c89424de2d",
    "photo-1584132967334-10e028bd69f7",
    "photo-1587574293340-e0011c4e8ecf",
    "photo-1590073844006-33379778ae09",
    "photo-1590490360182-c33d57733427",
    "photo-1590846406792-0adc7f938f1d",
    "photo-1592229505726-ca121723b8ef",
    "photo-1592861956120-e524fc739696",
    "photo-1595576508898-0ad5c879a061",
    "photo-1596436889106-be35e843f974",
    "photo-1611892440504-42a792e24d32",
    "photo-1615460549969-36fa19521a4f",
]
