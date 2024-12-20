1. Using [style.property] Binding
The [style.property] binding allows you to set a single CSS property directly.

<div [style.color]="'blue'" [style.font-size.px]="20">
  This text is styled with inline styles.
</div>

The color property is bound to 'blue'.
The font-size property is set to 20px (using the .px suffix).
2. Using [ngStyle] Directive
The [ngStyle] directive allows you to apply multiple inline styles dynamically.

<div [ngStyle]="{'color': 'green', 'font-size.px': 16}">
  This text uses ngStyle for multiple inline styles.
</div>

Using Component Properties:
typescript
Copy code
export class AppComponent {
  styles = {
    color: 'red',
    'font-size.px': 18,
    'background-color': 'lightyellow'
  };
}
<div [ngStyle]="styles">
  Inline styles from a component property.
</div>

Dynamic Styling with Conditions
You can dynamically change styles based on conditions or variables:

<div [style.color]="isHighlighted ? 'yellow' : 'black'">
  Conditional inline styling.
</div>

<div [ngStyle]="{ 'font-weight': isBold ? 'bold' : 'normal', 'color': textColor }">
  Dynamic styles with ngStyle.
</div>

export class AppComponent {
  isHighlighted = true;
  isBold = true;
  textColor = 'purple';
}

Key Points:
Use [style.property] for simple, single-property styles.
Use [ngStyle] for multiple styles or when dynamically applying many styles.
Ensure property names in [ngStyle] are in camelCase or kebab-case as needed.
Avoid overusing inline styles; prefer CSS classes for reusable styling.
