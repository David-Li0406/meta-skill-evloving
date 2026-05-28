export default function ComparisonMatrix({ data }) {
  return (
    <div className="p-6 bg-white rounded-xl shadow-lg">
      <h3 className="font-bold mb-4">Overall Score Comparison</h3>
      <div className="space-y-3">
        {data.map((item) => (
          <div key={item.name} className="flex items-center gap-3">
            <span className="w-32 text-sm font-medium">{item.name}</span>
            <div className="flex-1 bg-gray-100 rounded-full h-6 overflow-hidden">
              <div
                className={`h-full ${item.color} rounded-full transition-all duration-500`}
                style={{ width: `${item.score}%` }}
              />
            </div>
            <span className="w-12 text-right text-sm font-bold">{item.score}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
