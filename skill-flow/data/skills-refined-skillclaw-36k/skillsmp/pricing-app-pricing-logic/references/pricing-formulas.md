# Pricing Formulas Reference

Mathematical formulas and business logic for pricing calculations.

## Core Pricing Formula

```
1. Costo Base (ARS)
   = Costo USD × Tipo Cambio Venta (si moneda = USD)
   = Costo (si moneda = ARS)

2. Precio con Markup
   = Costo Base + (Costo Base × Markup%)

3. + Envío (opcional)
   = Precio con Markup + Costo Envío

4. + Comisión ML (tiered)
   = Precio + calcular_comision_ml_tiered(Precio)

5. + Varios (operational costs)
   = Precio + (Precio × Varios%)

6. Precio Final
   = Suma de todos los componentes

7. Ganancia Neta
   = Precio Final - Costo Base - Comisión ML - Varios - Envío

8. Margen %
   = (Ganancia Neta / Precio Final) × 100
```

## MercadoLibre Commission (Tiered)

```python
if precio <= MONTO_TIER1:
    comision = TIER1  # Fixed amount (e.g., $1095)
elif precio <= MONTO_TIER2:
    comision = TIER2  # Fixed amount (e.g., $2190)
elif precio <= MONTO_TIER3:
    comision = TIER3  # Fixed amount (e.g., $2628)
else:
    comision = precio × (COMISION_PORCENTAJE_ALTA / 100)
```

**Default Tiers (ejemplo):**
- Tier 1: Hasta $15.000 → $1.095
- Tier 2: Hasta $24.000 → $2.190
- Tier 3: Hasta $33.000 → $2.628
- Tier 4: Más de $33.000 → 12% del precio

## Installment Markup (Cuotas)

```python
markup_adicional = MARKUP_ADICIONAL_CUOTAS × CUOTAS_MULTIPLIER

Cuotas Multiplier:
- 3 cuotas  → 1.0x (4% adicional)
- 6 cuotas  → 1.5x (6% adicional)
- 9 cuotas  → 2.0x (8% adicional)
- 12 cuotas → 2.5x (10% adicional)

Precio con Cuotas = Precio Base + (Precio Base × markup_adicional / 100)
```

## Currency Conversion

```python
if moneda == "USD":
    tipo_cambio = get_tipo_cambio_venta(fecha=hoy)
    costo_ars = costo_usd × tipo_cambio
else:
    costo_ars = costo
```

**Tipo Cambio:**
- Source: `tb_cur_exch_history` table
- Tipo: `venta` (selling rate)
- Fallback: Latest available if today's missing

## Markup Calculation

**Priority order:**
1. **Product override** (if configured in `config_individual_productos`)
2. **Brand markup** (from `marcas_pm.porcentaje_markup`)
3. **Category/Subcategory group** (from commission group mapping)
4. **Default markup** (from `PricingConstants`)

```python
markup_final = producto.markup_override 
            or marca.porcentaje_markup
            or grupo.markup_default
            or constants.markup_default
```

## Shipping Cost

**Options:**
1. **Product-specific:** `producto.envio` field
2. **Group average:** Average of active products in same commission group
3. **Fixed fallback:** $500 (example)

```python
envio = producto.envio 
     or obtener_envio_promedio_grupo(grupo_id)
     or ENVIO_DEFAULT
```

## Varios (Operational Costs)

```python
varios_amount = precio_base × (VARIOS_PORCENTAJE / 100)
```

**Default:** 6.5% of base price

Covers:
- Payment processing fees
- Packaging costs
- Operational overhead

## Example Calculation

```
Producto: Notebook HP
Costo: USD $500
Tipo Cambio: $1.100 ARS/USD
Markup: 25%
Envío: $5.000
Comisión ML: Tier 2
Varios: 6.5%

1. Costo Base = $500 × $1.100 = $550.000
2. Precio Markup = $550.000 + ($550.000 × 0.25) = $687.500
3. + Envío = $687.500 + $5.000 = $692.500
4. + Comisión ML = $692.500 + $2.190 = $694.690
5. + Varios = $694.690 + ($694.690 × 0.065) = $739.844
6. Precio Final = $739.844 (redondeado a $740.000)
7. Ganancia Neta = $740.000 - $550.000 - $2.190 - $45.190 - $5.000 = $137.620
8. Margen = ($137.620 / $740.000) × 100 = 18.6%
```

## Database Tables

- `pricing_constants` - Versioned pricing config
- `tb_cur_exch_history` - Daily exchange rates
- `comision_versionada` - Versioned commission system
- `comision_base` - Base commissions per group/pricelist
- `subcategoria_grupo` - Subcategory → group mapping
- `marcas_pm` - Brand-specific markups
- `config_individual_productos` - Product-level overrides
