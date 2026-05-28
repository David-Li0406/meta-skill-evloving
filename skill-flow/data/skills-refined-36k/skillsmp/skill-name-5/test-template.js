const HelloWorld = () => console.log("Hello World")

const Sum = (a, b) => a + b

const SumClosure = () => (a) => Sum(a, 3)


console.log("Module loaded")

const sumar = SumClosure()

const resultado = sumar(4) + 2

const sumar2 = SumClosure()

const sum = Sum(5, 5)

const sum2 = Sum(8, 3)

console.log(sumar(4), sumar2(5), resultado, sum, sum2)

