export default function ABTestVariants({ control, variantA, variantB }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="text-center">
        <div className="text-sm font-medium text-gray-500 mb-2">Control</div>
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="font-bold text-sm mb-2">{control.title}</h3>
          <button className={`w-full py-2 ${control.buttonClass} text-white rounded`}>
            {control.buttonText}
          </button>
          {control.subtext && <p className="text-xs text-gray-500 mt-1">{control.subtext}</p>}
        </div>
        <div className="mt-2 text-xs text-gray-600">
          <div>CTR: {control.expectedCTR}</div>
        </div>
      </div>

      <div className="text-center">
        <div className="text-sm font-medium text-gray-500 mb-2">Variant A</div>
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="font-bold text-sm mb-2">{variantA.title}</h3>
          <button className={`w-full py-2 ${variantA.buttonClass} text-white rounded`}>
            {variantA.buttonText}
          </button>
          {variantA.subtext && <p className="text-xs text-gray-500 mt-1">{variantA.subtext}</p>}
        </div>
        <div className="mt-2 text-xs text-gray-600">
          <div className="text-green-600 font-semibold">+{variantA.expectedLift}% CTR</div>
        </div>
      </div>

      <div className="text-center">
        <div className="text-sm font-medium text-gray-500 mb-2">Variant B</div>
        <div className="p-4 bg-white rounded-lg shadow">
          <h3 className="font-bold text-sm mb-2">{variantB.title}</h3>
          <button className={`w-full py-2 ${variantB.buttonClass} text-white rounded`}>
            {variantB.buttonText}
          </button>
          {variantB.subtext && <p className="text-xs text-gray-500 mt-1">{variantB.subtext}</p>}
        </div>
        <div className="mt-2 text-xs text-gray-600">
          <div className="text-green-600 font-semibold">+{variantB.expectedLift}% CTR</div>
        </div>
      </div>
    </div>
  );
}
