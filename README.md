# Latex Parser

Converts Excel like equations to Latex with posibility of substitution, etc. for easy implementation to Word reports.

## Supported and tested mathematical functions:
ln- logarithm with base e
log- logarithm with base e
trigonometry functions that use radians
 -sin
 -cos
 -tan
Abs- absolute value of expression

## Constants, currently reserved variables
e- 2.72...
pi, π- 3.14... it is up to you to decide how will you write pi as a constant

## Symbolic numbers
<any latin, greek or numeric character>_<any latin, greek or numeric character>
String after underline goes to subscript, e.g.
μ_steel  ->  μ_{steel}
mu_steel ->  mu_{steel}