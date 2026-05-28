---
name: DDD Standard Architecture Rules
description: Comprehensive rules for DDD-based application architecture, including layer boundaries, dependency directions, state ownership, and strict separation of concerns between Domain, Application, Infrastructure, and Presentation layers.
license: MIT
---

# DDD Standard Architecture Rules

## 一、總體架構與分層定義

1. 系統必須明確劃分為 **Domain、Application、Infrastructure、Presentation** 四個層級。  
2. 每個檔案只能屬於一個層級，不得同時承擔多層責任。  
3. 分層的目的是隔離「業務意圖」與「技術細節」，不得為方便而合併層級。  
4. 架構設計必須以長期演進與替換成本最小化為目標。  

## 二、依賴方向（不可違反）

5. 只允許以下單向依賴：  
   **Domain → Application → Infrastructure → Presentation**  
6. 任何反向依賴一律視為架構錯誤。  
7. 不得以型別、工具函式、barrel export 或 side-effect 間接形成反向依賴。  
8. 依賴方向必須在 TypeScript `import` 層級即可被靜態分析出來。  

## 三、Domain 層規則（業務核心）

9. Domain 層必須是純 TypeScript。  
10. Domain 層不得依賴 Angular、RxJS、Signals、HTTP、Storage 或任何 framework。  
11. Domain 層不得有 `async / await`、`Promise` 或 I/O 行為。  
12. Domain 層只描述「業務是什麼」，不描述「怎麼做到」。  
13. Domain 層只能包含：  
    - Entity  
    - Value Object  
    - Domain Service  
    - Domain Interface  
14. Entity 必須具有明確身分識別（identity）。  
15. Value Object 必須是不可變（immutable）。  
16. Domain Service 只能表達無法自然歸屬於單一 Entity 的業務規則。  
17. Domain Interface 只描述能力，不描述實作方式。  
18. Domain 層不得知道資料來自哪裡、如何儲存、如何顯示。  

## 四、Application 層規則（業務流程與狀態協調）

19. Application 層負責「用例（Use Case）」與業務流程編排。  
20. Application 層是整個系統唯一的業務狀態真相持有者。  
21. Application 層可以依賴 Domain，但不得反向依賴 Presentation 或 Infrastructure 實作。  
22. Application 層只能依賴 Infrastructure **定義的 interface**，而非 concrete class。  
23. Application 層負責交易邊界（transaction boundary）與流程順序。  
24. Application 層不得包含 UI、DOM、Component、Template 相關概念。  
25. Application 層不得包含資料存取細節。  
26. Application 層不得將 framework 型別外洩給其他層。  
27. **Application Facade** 是 Presentation 唯一允許接觸的入口。  

## 五、Infrastructure 層規則（技術實作）

28. Infrastructure 層只負責實作 Domain 或 Application 定義的 interface。  
29. Infrastructure 層可以依賴 framework 與第三方套件。  
30. Infrastructure 層不得包含業務規則或決策邏輯。  
31. Infrastructure 層不得自行成為狀態真相。  
32. Infrastructure 層不得要求上層（Application / Domain）調整設計以配合技術細節。  
33. Infrastructure 層不得向外暴露 framework-specific 型別。  
34. Infrastructure 層可以被替換而不影響 Domain 與 Application。  

## 六、Presentation 層規則（UI 與互動）

35. Presentation 層只負責顯示與使用者互動。  
36. Presentation 層不得包含業務規則。  
37. Presentation 層不得自行定義業務狀態真相。  
38. Presentation 層只能依賴 Application Facade。  
39. Presentation 層不得直接呼叫 Infrastructure。  
40. Presentation 層不得繞過 Application 直接操作 Domain。  
41. Presentation 層的狀態只能是短生命週期的 UI state。  

## 七、狀態與責任邊界

42. Domain 層不持有應用狀態。  
43. Application 層集中管理所有業務狀態。  
44. Infrastructure 層不得持有長生命週期業務狀態。  
45. Presentation 層不得持有跨頁或跨流程的業務狀態。  
46. 任一狀態只能有單一權威來源（Single Source of Truth）。  

## 八、Interface 與抽象規則

47. Interface 的定義位置必須屬於需求方，而非實作方。  
48. Application 需要的能力，其 interface 必須定義在 Application 或 Domain。  
49. Infrastructure 只能實作 interface，不得反向定義需求。  
50. Interface 不得洩漏技術細節。  

## 九、Shared 與共用模組規則

51. `shared` 不得成為業務核心。  
52. `shared` 不得包含業務狀態或決策。  
53. 若 `shared` 被多個 feature 視為業務依賴，則其層級必須上移至 Application 或 Domain。  
54. `shared` 僅允許存在：  
    - 純工具  
    - 純 UI  
    - 純 stateless 元件  

## 十、結構與命名一致性

55. 資料夾結構必須反映分層與責任。  
56. 檔名與資料夾名稱必須能直接推斷其所屬層級。  
57. 不得出現語意與實際責任不符的命名。  
58. Barrel export 不得模糊層級邊界。  

## 十一、驗證與演進規則

59. Domain 必須能獨立於任何 framework 編譯與測試。  
60. Application 必須能在無 UI 的情況下運行與測試。  
61. Infrastructure 必須可被 mock 或替換。  
62. Presentation 的替換不得影響業務邏輯。  
63. 架構規則必須能透過 lint、test 或 CI 檢查。  
