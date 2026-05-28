
export interface BoldPricingProps {
  /** Main heading text */
  title?: string;
  /** Subtitle/description text */
  subtitle?: string;
  /** Price label (e.g., "Annual", "Monthly") */
  priceLabel?: string;
  /** Main price amount */
  price?: string;
  /** Price period (e.g., "/year", "/month") */
  pricePeriod?: string;
  /** Highlight text below price */
  highlightText?: string;
  /** Array of feature strings */
  features?: string[];
  /** Button text */
  buttonText?: string;
  /** Footer text array */
  footerText?: string[];
}

export default function BoldPricing({
  title = "One plan. Full access.",
  subtitle = "No tiers. No tricks. No \"contact sales.\"",
  priceLabel = "Annual",
  price = "$199",
  pricePeriod = "/year",
  highlightText = "Less than 4 lattes a month.",
  features = [
    "Unlimited projects",
    "100 GB storage",
    "Priority support",
    "Advanced analytics",
    "Custom integrations"
  ],
  buttonText = "Get Started →",
  footerText = [
    "90 days to decide. Take your time.",
    "Cancel from your account. No hoops."
  ],
}: BoldPricingProps) {
  return (
    <div className="bold-pricing">
      <h2>{title}</h2>
      <p>{subtitle}</p>

      <article>
        <small>{priceLabel}</small>
        <div className="price-row">
          <strong>{price}</strong> {pricePeriod}
        </div>
        <p className="highlight">{highlightText}</p>

        <ul>
          {features.map((feature, index) => (
            <li key={index}>{feature}</li>
          ))}
        </ul>

        <button>{buttonText}</button>
      </article>

      <footer>
        {footerText.map((text, index) => (
          <p key={index}>{text}</p>
        ))}
      </footer>
    </div>
  );
}