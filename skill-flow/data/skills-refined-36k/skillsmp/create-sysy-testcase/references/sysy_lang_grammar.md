# 2025编译技术实验文法定义及相关说明

## 概要

SysY 语言是编译技术实验所完成的编译器的源语言,是 C 语言的一个子集。一个 SysY 语言源程序文件中有且仅有一个名为 `main` 的主函数定义,除此之外包含若干全局变量声明、常量声明和其他函数定义。SysY 语言支持 32 位有符号数 `int` 类型及其的一维数组类型; `const` 修饰符用于声明常量。

SysY 语言本身没有提供输入/输出(I/O)的语言构造,I/O 是以运行时库方式提供,库函数可以在 SysY 程序中的函数内调用。部分 SysY 运行时库函数的参数类型会超出 SysY 支持的数据类型,如可以为字符串。SysY 编译器需要能处理这种情况,将 SysY 程序中这样的参数正确地传递给 SysY 运行时库。

*   **函数**: 函数可以带参数也可以不带参数,参数的类型可以是 `int` 或其一维数组类型;函数可以返回 `int` 类型的值,或者不返回值(即声明为 `void` 类型)。当参数为 `int` 时,按值传递;而参数为数组类型时,实际传递的是数组的起始地址。函数体由若干变量声明和语句组成。

*   **变量/常量声明**: 可以在一个变量/常量声明语句中声明多个变量或常量,声明时可以带初始化表达式。所有变量/常量要求先定义再使用。在函数外声明的为全局变量/常量,在函数内声明的为局部变量/常量。

*   **语句**: 语句包括赋值语句、表达式语句(表达式可以为空)、语句块、if 语句、for 语句、break语句、continue 语句、return 语句。语句块中可以包含若干变量声明和语句。

*   **表达式**: 支持基本的算术运算(`+`、`-`、`*`、`/`、`%`)、关系运算(`==`、`!=`、`<`、`>`、`<=`、`>=`)和逻辑运算(`!`、`&&`、`||`),非 0 表示真、0 表示假,而关系运算或逻辑运算的结果用 1 表示真、0 表示假。**算符的优先级和结合性以及计算规则(含逻辑运算的“短路计算”)与 C 语言一致**。

## 文法

### 语法定义

SysY 语言的文法采用扩展的 Backus 范式 (EBNF, Extended Backus-Naur Form) 表示,其中:

*   符号`[...]`表示方括号内包含的为可选项
*   符号`{...}`表示花括号内包含的为可重复 0 次或多次的项
*   终结符或者是由单引号括起的串,或者是 `Ident`、`IntConst`、`StringConst` 这样的记号
*   所有类似`'main'`这样的用单引号括起的字符串都是保留的关键字

SysY 语言的文法表示如下,其中 `CompUnit` 为开始符号:

**重要: 建议同时对照文法第三部分的语义约束。**

```
编译单元 CompUnit → {Decl} {FuncDef} MainFuncDef // 1.是否存在Decl 2.是否存在FuncDef

声明 Decl → ConstDecl | VarDecl // 覆盖两种声明

常量声明 ConstDecl → 'const' BType ConstDef { ',' ConstDef } ';' // 1.花括号内重复0次 2.花括号内重复多次

基本类型 BType → 'int'

常量定义 ConstDef → Ident [ '[' ConstExp ']' ] '=' ConstInitval // 包含普通变量、一维数组两种情况

常量初值 ConstInitval → ConstExp | '{' [ ConstExp { ',' ConstExp } ] '}' // 1.常表达式初值 2.一维数组初值

变量声明 VarDecl → [ 'static' ] BType VarDef { ',' VarDef } ';' // 1.花括号内重复0次 2.花括号内重复多次

变量定义 VarDef → Ident [ '[' ConstExp ']' ] | Ident [ '[' ConstExp ']' ] '=' Initval // 包含普通常量、一维数组定义

变量初值 InitVal → Exp | '{' [ Exp { ',' Exp } ] '}' // 1.表达式初值 2.一维数组初值

函数定义 FuncDef → FuncType Ident '(' [FuncFParams] ')' Block // 1.无形参 2.有形参

主函数定义 MainFuncDef → 'int' 'main' '(' ')' Block // 存在main函数

函数类型 FuncType → 'void' | 'int' // 覆盖两种类型的函数

函数形参表 FuncFParams → FuncFParam { ',' FuncFParam } // 1.花括号内重复0次 2.花括号内重复多次

函数形参 FuncFParam → BType Ident [ '[' ']' ] // 1.普通变量 2.一维数组变量

语句块 Block → '{' { BlockItem } '}' // 1.花括号内重复0次 2.花括号内重复多次

语句块项 BlockItem → Decl | Stmt // 覆盖两种语句块项

语句 Stmt → LVal '=' Exp ';' // 每种类型的语句都要覆盖
   | [Exp] ';' // 有无Exp两种情况;printf函数调用
   | Block
   | 'if' '(' Cond ')' Stmt [ 'else' Stmt ] // 1.有else 2.无else
   | 'for' '(' [ForStmt] ';' [Cond] ';' [ForStmt] ')' Stmt // 1. 无缺省,1种情况 2. ForStmt与Cond中缺省一个,3种情况 3. ForStmt与Cond中缺省两个,3种情况 4. ForStmt与Cond全部缺省,1种情况
   | 'break' ';'
   | 'continue' ';'
   | 'return' [Exp] ';' // 1.有Exp 2.无Exp
   | 'printf' '(' StringConst { ',' Exp } ')' ';' // 1.有Exp 2.无Exp

语句 ForStmt → LVal '=' Exp { ',' LVal '=' Exp } // 1.花括号内重复0次 2.花括号内重复多次

表达式 Exp → AddExp // 存在即可

条件表达式 Cond → LOrExp // 存在即可

左值表达式 LVal → Ident [ '[' Exp ']' ] // 1.普通变量、常量 2.一维数组

基本表达式 PrimaryExp → '(' Exp ')' | LVal | Number

数值 Number → IntConst // 存在即可

一元表达式 UnaryExp → PrimaryExp | Ident '(' [FuncRParams] ')' | UnaryOp UnaryExp // 3种情况均需覆盖,函数调用也需要覆盖FuncRParams的不同情况

单目运算符 UnaryOp → '+' | '-' | '!' //注:'!'仅出现在条件表达式中 // 三种均需覆盖

函数实参表达式 FuncRParams → Exp { ',' Exp } // 1.花括号内重复0次 2.花括号内重复多次 3.Exp需要覆盖数组传参和部分数组传参

乘除模表达式 MulExp → UnaryExp | MulExp ('*' | '/' | '%') UnaryExp // 1.UnaryExp 2.* 3./ 4.% 均需覆盖

加减表达式 AddExp → MulExp | AddExp ('+' | '-') MulExp // 1.MulExp 2.+ 需覆盖 3.- 需覆盖

关系表达式 RelExp → AddExp | RelExp ('<' | '>' | '<=' | '>=') AddExp // 1.AddExp 2.< 3.> 4.<= 5.>= 均需覆盖

相等性表达式 EqExp → RelExp | EqExp ('==' | '!=') RelExp // 1.RelExp 2.== 3.!= 均需覆盖

逻辑与表达式 LAndExp → EqExp | LAndExp '&&' EqExp // 1.EqExp 2.&& 均需覆盖

逻辑或表达式 LOrExp → LAndExp | LOrExp '||' LAndExp // 1.LAndExp 2.|| 均需覆盖

常量表达式 ConstExp → AddExp //注:使用的 Ident 必须是常量 // 存在即可
```

### 词法补充

#### (1) 标识符 Ident

SysY 语言中标识符 `Ident` 的规范如下 (identifier):

```
identifier → identifier-nondigit
           | identifier identifier-nondigit
           | identifier digit
```

其中, `identifier-nondigit` 为下划线或大小写字母, `digit` 为0到9的数字。

注: 请参考 ISO/IEC 9899 [http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf) 第 51 页关于标识符的定义**同名标识符**的约定:

*   全局变量(常量)和局部变量(常量)的作用域可以重叠,重叠部分局部变量(常量)优先;
*   同名局部变量的作用域不能重叠,即同一个 `Block` 内不能有同名的标识符(常量/变量);
*   在不同的作用域下,SysY 语言中变量(常量)名可以与函数名相同;
*   保留关键字不能作为标识符。

```c
// 合法样例
int main() {
    int a = 0;
    {
        int a = 1;
        printf("%d",a); // 输出 1
    }
    return 0;
}
```

```c
// 非法样例
int main() {
    int a = 0;
    {
        int a = 1;
        int a = 2; // 非法!
    }
    return 0;
}
```

#### (2) 注释

SysY 语言中注释的规范与 C 语言一致,如下:

*   **单行注释**: 以序列`'//'`开始,直到换行符结束,不包括换行符。
*   **多行注释**: 以序列`'/*'`开始,直到第一次出现`'*/'`时结束,包括结束处`'*/'`。

注: 请参考 ISO/IEC 9899 [http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf) 第 66 页关于注释的定义。

#### (3) 数值常量

SysY 语言中数值常量可以是整型数 `IntConst`,其规范如下(对应 integer-const):

```
整型常量 integer-const → decimal-const | 0

decimal-const → nonzero-digit | decimal-const digit

nonzero-digit 为1至9的数字。
```

注: 请参考 ISO/IEC 9899 [http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1124.pdf) 第 54 页关于整型常量的定义,在此基础上忽略所有后缀。

#### (4) 字符串常量

SysY 语言中 `<StringConst>` 的定义如下:

```
<FormatChar> → %d
<NormalChar> → 十进制编码为32,33,35-126的ASCII字符, '\' (编码92) 出现当且仅当为'\n'
<char> → <FormatChar> | <NormalChar>
<StringConst> → '"' {<char>} '"'
```

字符串中仅可能会出现一种转义字符`'\n'`,用以标注此处换行,其他转义情况无需考虑。

## 语义约束

符合上述文法的程序集合是合法的 SysY 语言程序集合的超集。下面进一步给出 SysY 语言的语义约束。

### 运行时库

1.  为了降低开发难度,保证所有测试程序中 `getint` 与 `printf` 只会作为运行时库调用出现,不会作为自定义的变量/函数标识符。
2.  `printf` 函数默认不换行。
3.  与 C 语言中的 `printf` 类似,输出语句中,格式字符将被替换为对应标识符,普通字符原样输出。

### static 关键字

1.  `static` 关键字用于修饰静态局部变量,不会在全局变量定义中出现。
2.  用 `static` 修饰的变量声明,若带有初始值,则初始值可在编译期内求出。
3.  用 `static` 修饰的变量声明,**即使在声明时未赋初值,编译器也会把它初始化为0**。
4.  `static` 关键字指定的变量只初始化一次,并在之后调用该函数时保留其状态,离开函数时不会被销毁。但其修饰的变量作用域被限制在声明此变量的函数内部。

### 编译单元 CompUnit

```
编译单元 CompUnit → {Decl} {FuncDef} MainFuncDef

声明 Decl → ConstDecl | VarDecl
```

1.  `CompUnit` 的顶层变量/常量声明语句(对应 `Decl`)、函数定义(对应 `FuncDef`)都不可以重复定义同名标识符(Ident),即便标识符的类型不同也不允许。
2.  `CompUnit` 的变量/常量/函数声明的作用域从该声明处开始到文件结尾。

### 常量定义 ConstDef

```
常量定义 ConstDef → Ident [ '[' ConstExp ']' ] '=' ConstInitVal
```

1.  `ConstDef` 用于定义符号常量。`ConstDef` 中的 `Ident` 为常量的标识符,在 `Ident` 后、`'='` 之前是可选的一维数组以及一维数组长度的定义部分,在`'='`之后是初始值。**常量必须有对应的初始值**。
2.  `ConstDef` 的一维数组以及一维数组长度的定义部分不存在时,表示定义单个变量。
3.  `ConstDef` 的一维数组以及一维数组长度的定义部分存在时,表示定义数组。其语义和 C 语言一致,每维的下界从 0 编号。
4.  `ConstDef` 中表示各维长度的 `ConstExp` 都必须能在编译时求值到**非负整数**。

### 变量定义 VarDef

```
变量定义 VarDef → Ident [ '[' ConstExp ']' ] | Ident [ '[' ConstExp ']' ] '=' Initval
```

1.  变量的定义与常量基本一致,但是变量可以没有初始值部分,此时其运行时实际初值未定义。

### 初值 ConstInitVal / InitVal

```
常量初值 ConstInitval → ConstExp | '{' [ ConstExp { ',' ConstExp } ] '}'

变量初值 Initval → Exp | '{' [ Exp { ',' Exp } ] '}'
```

1.  任何常量的初值表达式必须是常量表达式 `ConstExp`。
2.  常量必须有初始值,常量数组不需要每一个元素都有初始值,但是未赋值的部分编译器需要将其置0。
3.  全局变量的初值表达式也必须是常量表达式 `ConstExp`。但局部变量的初值表达式是 `Exp`,可以使用已经声明的变量。
4.  对于单个的常量或变量,初始值也必须是单个的表达式。(表达式包括单个数字、单个变量、单个常量等情况)
5.  对于全局变量,如果没有给出初始值,那么应该全部置0,局部变量不需要。

### 函数形参 FuncFParam 与实参 FuncRParams

```
函数形参表 FuncFParams → FuncFParam { ',' FuncFParam }
函数实参表 FuncRParams → Exp { ',' Exp }
```

1.  `FuncFParam` 定义一个函数的一个形式参数。当`Ident` 后面的可选部分存在时,表示数组定义。
2.  函数实参的语法是 `Exp`。对于普通变量,遵循按值传递;对于数组类型的参数,则形参接收的是实参数组的地址,并通过地址间接访问实参数组中的元素。
3.  普通常量可以作为函数参数,但是常量数组不可以,如 `const int arr[3] = {1,2,3}`,常量数组 `arr` **不能**作为参数传入到函数中。
4.  函数调用时要保证实参类型和形参类型一致,具体请看下面例子。

```c
void f1(int x) {
    return;
}
void f2(int x[]) {
    return;
}

int main() {
    int x = 10;
    int t[5] = {1, 2, 3, 4, 5};
    f1(x);      // 合法
    f1(t[0]);   // 合法
    f1(t);      // 不合法
    f2(t);      // 合法
}
```

### 函数定义 FuncDef

```
函数定义 FuncDef → FuncType Ident '(' [FuncFParams] ')' Block
```

1.  `FuncDef` 表示函数定义。其中的 `FuncType` 指明返回类型。当返回类型为 `int` 时,函数内所有分支都应当含有带有 `Exp` 的 `return` 语句。不含有 `return` 语句的分支的返回值未定义。当返回值类型为 `void` 时,函数内只能出现不带返回值的 `return` 语句。
2.  `FuncFParams` 的语义如前文。

### 语句块 Block

1.  `Block` 表示语句块。语句块会创建作用域,语句块内声明的常量和变量的生存期在该语句块内。
2.  语句块内可以再次定义与语句块外同名的变量或常量(通过 `Decl` 语句),其作用域从定义处开始到该语句块尾结束,它隐藏语句块外的同名变量或常量。
3.  为了降低开发难度,**保证所有测试程序中有返回值的函数 Block 的最后一句一定会显式的给出 return 语句**,否则就当作“无返回语句”的错误处理。同时,同学们编写上传的样例程序时,也需要保证这一点。
4.  `main` 函数的返回值只能为常数0。

### 语句 Stmt

1.  `Stmt` 中的 `if` 类型语句遵循就近匹配。
2.  单个 `Exp` 可以作为 `Stmt`。这个 `Exp` 会被求值,但是所求的值会被丢弃。

### 左值 LVal

1.  `LVal` 表示具有左值的表达式,可以为变量或者某个数组元素。
2.  当 `LVal` 表示数组时,方括号个数必须和数组变量的维数相同(即定位到元素)。
3.  当 `LVal` 表示单个变量时,不能出现后面的方括号。

### Exp 与 Cond

1.  `Exp` 在 SysY 中代表 `int` 型表达式;`Cond` 代表条件表达式,故它定义为 `LOrExp`。前者的单目运算符中不出现`'!'`,后者可以出现。
2.  `LVal` 必须是当前作用域内、该 `Exp` 语句之前有定义的变量或常量;对于赋值号左边的 `LVal` 必须是变量。
3.  函数调用形式是 `Ident '(' FuncRParams ')'`,其中的 `FuncRParams` 表示实际参数。实际参数的类型和个数必须与`Ident` 对应的函数定义的形参完全匹配。
4.  SysY 中算符的优先级与结合性与 C 语言一致,在上面的 SysY 文法中已体现出优先级与结合性的定义。

### 一元表达式 UnaryExp

1.  相邻两个 `UnaryOp` 不能相同,如 `int a = ++-i;` ,但是 `int a = +-+i;` 是可行的。
2.  `UnaryOp` 为`'!'`只能出现在条件表达式中。

### 常量表达式 ConstExp

1.  `ConstExp` 在 SysY 中代表 `int` 型表达式。
2.  `ConstExp` 在编译期内是可被求值的,`ConstExp` -> `AddExp` 中涉及到的的 `ident` 均必须是常量,即只能使用常数、可以取得具体值的常量以及由它们组成的、在编译器内可被求值的算术表达式。

