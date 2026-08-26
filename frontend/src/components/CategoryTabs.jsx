export default function CategoryTabs({ categories, activeId, onSelect }) {
  return (
    <div className="sticky top-[57px] z-20 flex gap-2 overflow-x-auto bg-[#f5f5f5] px-4 py-3">
      <button
        onClick={() => onSelect(null)}
        className={`shrink-0 rounded-full px-4 py-1.5 text-sm font-semibold ${
          activeId === null ? "bg-zomato text-white" : "bg-white text-gray-700 shadow"
        }`}
      >
        All
      </button>
      {categories.map((cat) => (
        <button
          key={cat.id}
          onClick={() => onSelect(cat.id)}
          className={`shrink-0 rounded-full px-4 py-1.5 text-sm font-semibold ${
            activeId === cat.id ? "bg-zomato text-white" : "bg-white text-gray-700 shadow"
          }`}
        >
          {cat.name}
        </button>
      ))}
    </div>
  );
}
