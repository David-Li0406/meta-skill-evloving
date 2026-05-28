export default function FeatureMatrix({ features }) {
  const [highlight, setHighlight] = React.useState(null);
  
  const Check = () => <span className="text-green-600 text-lg">✓</span>;
  const Cross = () => <span className="text-red-400 text-lg">✗</span>;
  
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b-2">
            <th className="py-2 text-left">Feature</th>
            <th className="py-2 text-center bg-blue-50">Us</th>
            <th className="py-2 text-center">Competitor A</th>
            <th className="py-2 text-center">Competitor B</th>
            <th className="py-2 text-center">Competitor C</th>
          </tr>
        </thead>
        <tbody>
          {features.map((f, i) => (
            <tr
              key={f.name}
              className={`border-b ${highlight === i ? 'bg-yellow-50' : ''}`}
              onMouseEnter={() => setHighlight(i)}
              onMouseLeave={() => setHighlight(null)}
            >
              <td className="py-2 font-medium">{f.name}</td>
              <td className="py-2 text-center bg-blue-50">{f.ours ? <Check /> : <Cross />}</td>
              <td className="py-2 text-center">{f.compA ? <Check /> : <Cross />}</td>
              <td className="py-2 text-center">{f.compB ? <Check /> : <Cross />}</td>
              <td className="py-2 text-center">{f.compC ? <Check /> : <Cross />}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
