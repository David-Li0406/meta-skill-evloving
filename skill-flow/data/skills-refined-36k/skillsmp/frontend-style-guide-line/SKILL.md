---
name: frontend-style-guide-line
description: Это требования по стилю и архитектуре написания кода для frontend приложений
---

# Общие требования

- **Стек технологий**: Все frontend-приложения и библиотеки должны быть написаны исключительно на языке **TypeScript**.
- **Качество кода**: Все форматирование и статический анализ кода должны быть строго настроены через **Prettier** и **ESLint**. Код должен соответствовать правилам проекта без предупреждений (warnings).
- **Документирование**: Все ключевые объекты кода (интерфейсы, классы, методы, типы) по возможности должны иметь описание в стиле **JSDoc**. Это критично для понимания назначения функций и параметров.

<example>
/**
 * Выполняет расчет итоговой стоимости заказа.
 * @param items - массив позиций заказа
 * @param discount - применимый коэффициент скидки (0..1)
 * @returns итоговая сумма в копейках
 */
const calculateTotalDelegate = (items: IItem[], discount: number): number => {
  // ...
};
</example>

# Общие принципы созданию кода

## Базовые принципы
- **Null vs Undefined**: Всегда отдавать предпочтение `undefined`. Использование `null` допускается только при сравнении с ним и в исключительных случаях (например, при взаимодействии с внешними API, где это критично).
- **Const Assertion**: Всегда использовать `as const` для readonly-массивов и глобальных константных объектов.
- **Взаимосвязанные функции**: По логике C#, группировать такие функции в `abstract class` с префиксом `Helper` и публичными статическими методами.

## C#-like Development Standards
- **Explicit Visibility**: Каждый метод или поле ОБЯЗАНЫ иметь модификатор `public`, `private` или `protected`.
- **Encapsulation**: Публичные данные должны быть `readonly` или реализованы через `get/set`. Напрямую изменять поля класса извне запрещено.
- **Async/Await**: Все асинхронные методы должны возвращать `Promise<T>` и иметь суффикс `Async` (например, `fetchDataAsync`).
- **No Any**: Использование `any` приравнивается к ошибке. Используй `unknown` и механизмы `castTo`.

## Дополнительные стандарты качества
- **Return Types**: Всегда явно объявлять тип возвращаемого значения (напр. `public getItems(): IItem[]`).
- **Error Handling**: Для сложных операций предпочитать возврат объекта результата `{ success: boolean, data?: T }` вместо генерации исключений.
- **Async Suffix**: Все асинхронные методы (возвращающие Promise) должны иметь суффикс `Async` (напр. `loadDataAsync`).
- **No Magic Values**: Любые конфигурационные значения должны быть вынесены в `abstract class ...Constants`.


# Требования к наименованию типов

- **Общий стиль**: Использовать **PascalCase** для всех названий типов, интерфейсов и классов.

- **Интерфейсы**: Все интерфейсы (interfaces) **обязательно** должны иметь префикс `I`.
    - *Пример:* `interface IUser { ... }`

- **Функциональные типы**: Все типы, объявляющие сигнатуру функции (function types), **обязательно** должны иметь суффикс `Delegate` или `Function`.
    - *Пример:* `type ChangeHandlerDelegate = (value: string) => void;`

- **Литеральные строковые типы**:
    - Должны иметь префикс `T` (например, `type TStatus = "open" | "closed"`).
    - **Важно**: Все строковые значения внутри литеральных типов должны быть только в **нижнем регистре** (lowercase).

- **Статические классы**:
    - Классы, содержащие только `static readonly` данные, должны быть **абстрактными** (`abstract`) и иметь суффикс `Constants`.
    - Классы, содержащие только статические методы, должны быть **абстрактными** (`abstract`) и иметь суффикс `Helper` или `Utils`.

<example>
// ✅ Правильно
interface IProject { id: number; }
type TTheme = "light" | "dark";
type TSizeOptions = "small" | "large";
type OnUploadDelegate = (file: File) => Promise<void>;

abstract class APIConstants {
  static readonly BASE_URL = "https://api.com";
}

abstract class StringHelper {
  static capitalize(str: string) { ... }
}

// ❌ Неправильно
interface User { ... } // Пропущен префикс I
type Status = "Open" | "Closed"; // Нет T, значения не в lowercase
type ClickHandler = () => void; // Нет суффикса Delegate

class AppConfig { // Должен быть abstract и с суффиксом Constants
  static readonly VERSION = "1.0";
}
</example>


# Требования к членам класса

- **Константы**: Статические публичные `readonly` данные (константы класса) должны быть в стиле **PascalCase**.
- **Приватные поля**: Все приватные члены класса (fields/properties) должны начинаться с префикса нижнего подчеркивания `_` (напр. `_items`).
- **Объявление полей**: Все поля класса должны быть явно объявлены, иметь модификатор доступа (`public`, `private`, `protected`) и быть проинициализированы (в месте объявления или в конструкторе).
- **Группировка и порядок регионов**: Все члены класса должны быть обернуты в `#region` / `#endregion`. Регионы должны следовать строго в указанном порядке:
    1. `Instance` (только для классов, реализующих паттерн ClassInstance)
    2. `Static fields`
    3. `Static properties`
    4. `Fields`
    5. `Properties`
    6. `Constructors`
    7. `Methods` (для обычных методов класса)
    8. `[Имя интерфейса]` (для реализации методов конкретного интерфейса)

**Исключение**: Если класс содержит только один тип членов (например, только `static readonly` поля, только статические методы, или только поля), использование регионов не является обязательным. Регионы необходимы для классов с несколькими типами членов для улучшения читаемости и структурирования кода.

<example>
class DataManager implements IDisposable {
  #region Static fields
  public static readonly DefaultTimeout = 5000;
  #endregion

  #region Static properties
  static get InstanceName() { return "DataManager"; }
  #endregion

  #region Fields
  private _isActive: boolean = false;
  #endregion

  #region Properties
  get isActive() { return this._isActive; }
  #endregion

  #region Constructors
  constructor() {
    this._isActive = true;
  }
  #endregion

  #region Methods
  private _internalHelper() {
    // внутренняя логика
  }
  #endregion

  #region IDisposable
  public dispose() {
    this._isActive = false;
  }
  #endregion
}
</example>

- **Паттерн ClassInstance**:
    - Реализация должна соответствовать примеру ниже.
    - Приватное статическое поле для хранения экземпляра (`private static _НАЗВАНИЕ_КЛАССА_В_CAMEL_CASE: T;`).
    - Публичный статический геттер `Instance` для доступа и ленивой инициализации.
    - Регион `#region Instance` должен быть **первым** в классе.
<example>
export class DelimiterCommand
{
  // #region Instance
  private static _delimiterCommand: DelimiterCommand;

  public static get Instance(): DelimiterCommand
  {
    return this._delimiterCommand || (this._delimiterCommand = new this(TActionCommandTypes.Delimiter));
  }
  // #endregion

  constructor(name: string) 
  {
    super(TActionCommandTypes.Delimiter, name);
  }
}
</example>


# Требование к наименованию и объявлению глобальных объектов

- **Глобальные константы**: Постоянные объекты и массивы, объявленные вне классов или функций (на уровне модуля), должны быть написаны в стиле **PascalCase**. 
- **Неизменяемость**: Рекомендуется использовать `as const` для обеспечения полной типизации значений.

<example>
// ✅ Правильно
export const AppConfiguration = {
  ApiUrl: "https://api.example.com",
  Timeout: 3000
} as const;

export const DefaultUserRoles = ["admin", "editor", "viewer"] as const;

// ❌ Неправильно
export const app_config = { ... }; // Не PascalCase
export const APP_CONFIG = { ... }; // Не PascalCase (SCREAMING_SNAKE_CASE не используется)

# Обязательные паттерны реализации

## Паттерн "Интерфейс + Type Guard + Caster"
Для каждого интерфейса TypeScript должны быть реализованы и экспортированы в том же файле две функции:
1. `instanceOf[Name]` — Type Guard для проверки реализации интерфейса.
2. `castTo[Name]` — Безопасное преобразование (возвращает объект или `undefined`).

<example>
export interface IEditable {
  id: TKey;
}

export function instanceOfEditable(value: unknown): value is IEditable {
  return (value && typeof value === 'object' && 'id' in value);
}

export function castToEditable(value: unknown): IEditable | undefined {
  return instanceOfEditable(value) ? value : undefined;
}
</example>

## Паттерн "CustomEvent"
События `CustomEvent` должны строго следовать структуре:
- `[Name]EventType` — строковая константа типа.
- `I[Name]EventData` — интерфейс данных в `detail`.
- `[Name]Event` — тип самого события (`CustomEvent<I...Data>`).
- `create[Name]Event` — фабричная функция для создания события.

<example>
export const LanguageChangeEventType = 'LanguageChangeEventType' as const;

export interface ILanguageChangeEventData {
  lang: TLanguageType;
}

export type LanguageChangeEvent = CustomEvent<ILanguageChangeEventData>;

export const createLanguageChangeEvent = (lang: TLanguageType): Event => {
  const data: ILanguageChangeEventData = { lang };
  return new CustomEvent<ILanguageChangeEventData>(LanguageChangeEventType, { detail: data });
};
</example>

## Паттерн "EnumClass" (Enum-like Objects)
Реализация строковых перечислений должна содержать три сущности:
1. `T[Name]Values` — readonly массив строк (as const).
2. `T[Name]` — alias литерального типа.
3. `T[Name]s` — объект-обертка (с суффиксом множественного числа и ключами в PascalCase), содержащий методы: `getAllValues`, `is[Name]`, `getByIndex`, `getByName`.

<example>
export const TActionCommandTypeValues = ['default', 'navigation', 'delimiter'] as const;
export type TActionCommandType = (typeof TActionCommandTypeValues)[number];

export const TActionCommandTypes = {
  Default: TActionCommandTypeValues[0],
  Navigation: TActionCommandTypeValues[1],
  Delimiter: TActionCommandTypeValues[2],

  getAllValues(): typeof TActionCommandTypeValues {
    return TActionCommandTypeValues;
  },
  isActionCommandType(value: any): value is TActionCommandType {
    return TActionCommandTypeValues.includes(value);
  },
  getByIndex(index: number): TActionCommandType | undefined {
    return TActionCommandTypeValues[index];
  },
  getByName(name: string): TActionCommandType | undefined {
    return TActionCommandTypeValues.find((v) => v === name);
  }
} as const;
</example>

















