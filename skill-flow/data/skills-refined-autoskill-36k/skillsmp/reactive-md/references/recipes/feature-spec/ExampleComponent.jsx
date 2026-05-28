export default function ExampleComponent({ 
  title = "Interactive Example",
  buttonLabel = "Toggle",
  isActive: initialActive = false,
  onStateChange = () => {}
}) {
  const [active, setActive] = React.useState(initialActive);
  
  const handleToggle = () => {
    const newState = !active;
    setActive(newState);
    onStateChange(newState);
  };
  
  return (
    <div className="p-4 border border-gray-300 rounded">
      <h3 className="font-bold mb-4">{title}</h3>
      <button 
        onClick={handleToggle}
        className={`px-4 py-2 rounded text-white transition-colors ${
          active ? 'bg-green-500 hover:bg-green-600' : 'bg-gray-400 hover:bg-gray-500'
        }`}
      >
        {buttonLabel}: {active ? 'Active' : 'Inactive'}
      </button>
    </div>
  );
}
