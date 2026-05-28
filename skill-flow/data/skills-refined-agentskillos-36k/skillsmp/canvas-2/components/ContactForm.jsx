/**
 * ContactForm - Validated form with customizable fields
 *
 * @prop {string} title - Form heading (default: "Contact Us")
 * @prop {string} description - Form description (default: "We'll get back to you soon.")
 * @prop {Array} fields - Field definitions (default: email + message)
 *   Each field: { name, type, label, required, placeholder, validation }
 *   Types: "text", "email", "tel", "textarea", "select"
 *   For select: add options: [{value, label}]
 * @prop {function} onSubmit - Called with form data on valid submit (default: emits 'form-submit')
 * @prop {string} submitLabel - Submit button text (default: "Submit")
 * @prop {string} successMessage - Message shown after submit (default: "Thank you! Your message has been sent.")
 * @prop {boolean} showReset - Show reset button (default: true)
 * @prop {string} className - Additional CSS classes for the card
 */
function ContactForm({
  title = "Contact Us",
  description = "We'll get back to you soon.",
  fields = [
    { name: "email", type: "email", label: "Email", required: true, placeholder: "you@example.com" },
    { name: "message", type: "textarea", label: "Message", required: true, placeholder: "How can we help?" }
  ],
  onSubmit,
  submitLabel = "Submit",
  successMessage = "Thank you! Your message has been sent.",
  showReset = true,
  className = ""
}) {
  const [formData, setFormData] = useState(() => {
    const initial = {}
    fields.forEach(f => { initial[f.name] = "" })
    return initial
  })
  const [errors, setErrors] = useState({})
  const [submitted, setSubmitted] = useState(false)

  const validate = () => {
    const newErrors = {}

    fields.forEach(field => {
      const value = formData[field.name]

      if (field.required && !value?.toString().trim()) {
        newErrors[field.name] = `${field.label || field.name} is required`
        return
      }

      if (value && field.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        newErrors[field.name] = "Please enter a valid email"
        return
      }

      if (value && field.type === "tel" && !/^\+?[\d\s\-()]+$/.test(value)) {
        newErrors[field.name] = "Please enter a valid phone number"
        return
      }

      if (field.validation && value) {
        const error = field.validation(value, formData)
        if (error) newErrors[field.name] = error
      }
    })

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleChange = (name) => (e) => {
    const value = e.target.type === "checkbox" ? e.target.checked : e.target.value
    setFormData(prev => ({ ...prev, [name]: value }))
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: undefined }))
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validate()) {
      const data = { ...formData, timestamp: new Date().toISOString() }
      if (onSubmit) {
        onSubmit(data)
      } else {
        window.canvasEmit("form-submit", data)
      }
      setSubmitted(true)
    }
  }

  const handleReset = () => {
    const initial = {}
    fields.forEach(f => { initial[f.name] = "" })
    setFormData(initial)
    setErrors({})
    setSubmitted(false)
  }

  const renderField = (field) => {
    const { name, type, label, required, placeholder, options } = field
    const value = formData[name] || ""
    const error = errors[name]
    const baseClass = "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
    const errorClass = error ? "border-red-500" : ""

    if (type === "textarea") {
      return (
        <div key={name} className="space-y-2">
          <Label htmlFor={name}>{label}{required && " *"}</Label>
          <textarea
            id={name}
            placeholder={placeholder}
            value={value}
            onChange={handleChange(name)}
            className={cn(baseClass, "min-h-[80px] h-auto py-2", errorClass)}
            rows={4}
          />
          {error && <p className="text-sm text-red-500">{error}</p>}
        </div>
      )
    }

    if (type === "select") {
      return (
        <div key={name} className="space-y-2">
          <Label htmlFor={name}>{label}{required && " *"}</Label>
          <select
            id={name}
            value={value}
            onChange={handleChange(name)}
            className={cn(baseClass, errorClass)}
          >
            <option value="">{placeholder || `Select ${label}`}</option>
            {(options || []).map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
          {error && <p className="text-sm text-red-500">{error}</p>}
        </div>
      )
    }

    return (
      <div key={name} className="space-y-2">
        <Label htmlFor={name}>{label}{required && " *"}</Label>
        <Input
          id={name}
          type={type || "text"}
          placeholder={placeholder}
          value={value}
          onChange={handleChange(name)}
          className={errorClass}
        />
        {error && <p className="text-sm text-red-500">{error}</p>}
      </div>
    )
  }

  if (submitted) {
    return (
      <Card className={cn("w-full max-w-md mx-auto", className)}>
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 p-4 bg-green-50 border border-green-200 rounded-md">
            <Check className="h-4 w-4 text-green-600" />
            <p className="text-green-800">{successMessage}</p>
          </div>
          {showReset && (
            <Button onClick={handleReset} className="w-full mt-4" variant="outline">
              Submit Another
            </Button>
          )}
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className={cn("w-full max-w-md mx-auto", className)}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {fields.map(renderField)}
        </CardContent>
        <CardFooter className="flex gap-2">
          {showReset && (
            <Button type="button" variant="outline" onClick={handleReset}>
              Clear
            </Button>
          )}
          <Button type="submit" className="flex-1">
            {submitLabel}
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
}
