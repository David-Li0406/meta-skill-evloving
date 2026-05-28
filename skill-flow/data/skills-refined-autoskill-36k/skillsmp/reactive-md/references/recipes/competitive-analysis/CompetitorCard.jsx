export default function CompetitorCard({ 
  name = "Competitor",
  features = [],
  strengths = [],
  weaknesses = [],
  pricing = "Contact sales"
}) {
  return (
    <div className="border border-gray-300 rounded-lg p-6 bg-white">
      <h3 className="text-lg font-bold mb-4">{name}</h3>
      
      <div className="mb-4">
        <h4 className="font-semibold text-green-700 mb-2">Strengths:</h4>
        <ul className="list-disc list-inside space-y-1">
          {strengths.map((s, i) => (
            <li key={i} className="text-sm text-green-600">{s}</li>
          ))}
        </ul>
      </div>
      
      <div className="mb-4">
        <h4 className="font-semibold text-red-700 mb-2">Weaknesses:</h4>
        <ul className="list-disc list-inside space-y-1">
          {weaknesses.map((w, i) => (
            <li key={i} className="text-sm text-red-600">{w}</li>
          ))}
        </ul>
      </div>
      
      <div className="mb-4">
        <h4 className="font-semibold mb-2">Key Features:</h4>
        <ul className="list-disc list-inside space-y-1">
          {features.map((f, i) => (
            <li key={i} className="text-sm text-gray-700">{f}</li>
          ))}
        </ul>
      </div>
      
      <div className="pt-4 border-t">
        <p className="text-sm"><span className="font-semibold">Pricing:</span> {pricing}</p>
      </div>
    </div>
  );
}
