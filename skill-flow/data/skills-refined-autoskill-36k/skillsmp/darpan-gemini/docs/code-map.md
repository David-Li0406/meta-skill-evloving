# Code Map

This wiki lives in `runtime/component/darpan/darpan.wiki`. The Darpan component code is in `runtime/component/darpan`.

## Start Here

- Component descriptor: `runtime/component/darpan/component.xml`
- Entities (party + reconciliation config): `runtime/component/darpan/entity/PartyEntities.xml`, `runtime/component/darpan/entity/ReconciliationEntities.xml`, `runtime/component/darpan/entity/MappingEntities.xml`
- Service definitions: `runtime/component/darpan/service/ReconciliationCsvServices.xml`, `runtime/component/darpan/service/ReconciliationCoreServices.xml`, `runtime/component/darpan/service/ReconciliationSampleServices.xml`, `runtime/component/darpan/service/JsonSchemaServices.xml`
- Script implementations: unified reconciliation in `runtime/component/darpan/src/reconciliation/core/reconcileUnifiedFiles.groovy`, mapping router in `runtime/component/darpan/src/reconciliation/core/reconcileFilesByMapping.groovy`, sample compare in `runtime/component/darpan/src/reconciliation/sample/compareSampleOrderIds.groovy`, JSON schema helpers in `runtime/component/darpan/src/jsonschema/createJsonSchemaFromJson.groovy`, `runtime/component/darpan/src/jsonschema/saveJsonSchema.groovy`, `runtime/component/darpan/src/jsonschema/validateJsonFileAgainstSchema.groovy`
- Generic reconciliation diff view actions: `runtime/component/darpan/screen/Reconciliation/GenericReconciliation/GenericReconciliationView/GenericReconciliationViewActions.groovy`, `runtime/component/darpan/screen/Reconciliation/GenericReconciliation/GenericReconciliationView/MissingJsonListActions.groovy`
- BOM cycle check: `runtime/component/darpan/service/BomServices.xml`, script `runtime/component/darpan/src/bom/runBomCycleCheck.groovy`, screen `runtime/component/darpan/screen/Reconciliation/BomCycleCheck.xml`
- Sample data inputs: `runtime/component/darpan/data/sample/omsBulkData.json`, `runtime/component/darpan/data/sample/shopifyBulkData.json`
- Build config: `runtime/component/darpan/build.gradle`

## Reconciliation Implementation Pointers

- Configuration entities (Reconciliation, ReconciliationRun, RunDataDocument, RunSystemInstance, RuleSet, Rule) are defined in
  `runtime/component/darpan/entity/ReconciliationEntities.xml`.
- The sample comparison flow uses Spark to anti-join OMS vs Shopify bulk exports in
  `runtime/component/darpan/src/reconciliation/sample/compareSampleOrderIds.groovy`.
- The sample service that runs the script is `compare#SampleOrderIds` in
  `runtime/component/darpan/service/ReconciliationSampleServices.xml`.

## Framework References

- DataDocument entity (used by RunDataDocument) lives in `framework/entity/EntityEntities.xml`.
- SystemMessageRemote entity (used by RunSystemInstance) lives in `framework/entity/ServiceEntities.xml`.
