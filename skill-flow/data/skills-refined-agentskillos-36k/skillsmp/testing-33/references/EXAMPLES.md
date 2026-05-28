# Примеры тестирования

## Unit-тесты ViewModels с MockK

### Базовый пример

```kotlin
class MainScreenViewModelTest {

    private lateinit var viewModel: MainScreenViewModel
    private val mockRepository: ItemRepository = mockk()

    @Before
    fun setup() {
        // Настраиваем поведение моков перед каждым тестом
        every { mockRepository.getAllItems() } returns flowOf(listOf(testItem))
        viewModel = MainScreenViewModel(mockRepository)
    }

    @Test
    fun loadItems_whenRepositoryReturnsData_thenSuccessState() {
        // Given
        val expectedItems = listOf(testItem)
        every { mockRepository.getAllItems() } returns flowOf(expectedItems)

        // When
        viewModel.loadItems()

        // Then
        assertEquals(MainScreenState.Success(expectedItems), viewModel.uiState.value)
    }

    @Test
    fun loadItems_whenRepositoryReturnsEmpty_thenEmptyState() {
        // Given
        every { mockRepository.getAllItems() } returns flowOf(emptyList())

        // When
        viewModel.loadItems()

        // Then
        assertEquals(MainScreenState.Empty, viewModel.uiState.value)
    }

    @Test
    fun deleteItem_whenCalled_thenRepositoryDeleteInvoked() {
        // When
        viewModel.deleteItem(testItem)

        // Then
        verify { mockRepository.deleteItem(testItem) }
    }

    private companion object {
        val testItem = Item(
            id = 1L,
            title = "Тест",
            details = "Описание",
            timestamp = System.currentTimeMillis(),
            colorTag = 0xFFFF00.toInt(),
            displayOption = DisplayOption.DAY
        )
    }
}
```

### Unit-тест с StateFlow и Turbine

```kotlin
class DetailScreenViewModelTest {

    private lateinit var viewModel: DetailScreenViewModel
    private val mockRepository: ItemRepository = mockk()
    private val mockLogger: Logger = NoOpLogger()

    @Before
    fun setup() {
        viewModel = DetailScreenViewModel(mockRepository, mockLogger, SavedStateHandle())
    }

    @Test
    fun loadItem_whenItemExists_thenEmitsSuccessState() = runTest {
        // Given
        val testItem = testItem()
        coEvery { mockRepository.getItemById(1L) } returns testItem

        // When
        viewModel.loadItem(1L)

        // Then - используем Turbine для тестирования StateFlow
        viewModel.uiState.test {
            val loadingState = awaitItem()
            assertTrue(loadingState is DetailScreenState.Loading)

            val successState = awaitItem()
            assertTrue(successState is DetailScreenState.Success)
            assertEquals(testItem, (successState as DetailScreenState.Success).item)
        }
    }

    @Test
    fun loadItem_whenItemNotFound_thenEmitsErrorState() = runTest {
        // Given
        coEvery { mockRepository.getItemById(1L) } returns null

        // When
        viewModel.loadItem(1L)

        // Then
        viewModel.uiState.test {
            val loadingState = awaitItem()
            assertTrue(loadingState is DetailScreenState.Loading)

            val errorState = awaitItem()
            assertTrue(errorState is DetailScreenState.Error)
        }
    }
}
```

## Интеграционные тесты DAO и Repository

### Интеграционный тест DAO

```kotlin
@RunWith(AndroidJUnit4::class)
class ItemDaoTest {

    private lateinit var database: DaysDatabase
    private lateinit var dao: ItemDao

    @Before
    fun createDb() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        database = Room.inMemoryDatabaseBuilder(
            context,
            DaysDatabase::class.java
        ).allowMainThreadQueries().build()
        dao = database.itemDao()
    }

    @After
    fun closeDb() {
        database.close()
    }

    @Test
    fun insertItem_whenInsert_thenCanRetrieve() = runBlocking {
        // Given
        val item = testItem()

        // When
        dao.insert(item)
        val retrieved = dao.getById(item.id)

        // Then
        assertNotNull(retrieved)
        assertEquals(item.title, retrieved!!.title)
    }

    @Test
    fun getAllItems_whenMultipleItems_thenReturnsAll() = runBlocking {
        // Given
        val items = listOf(
            testItem(id = 1L, title = "Первый"),
            testItem(id = 2L, title = "Второй"),
            testItem(id = 3L, title = "Третий")
        )
        items.forEach { dao.insert(it) }

        // When
        val retrievedItems = dao.getAll()

        // Then
        assertEquals(3, retrievedItems.size)
        assertEquals("Первый", retrievedItems[0].title)
    }

    @Test
    fun deleteItem_whenDeleted_thenCannotRetrieve() = runBlocking {
        // Given
        val item = testItem()
        dao.insert(item)
        assertNotNull(dao.getById(item.id))

        // When
        dao.delete(item)
        val retrieved = dao.getById(item.id)

        // Then
        assertNull(retrieved)
    }

    private fun testItem(
        id: Long = 1L,
        title: String = "Тест"
    ) = ItemEntity(
        id = id,
        title = title,
        details = "Описание",
        timestamp = System.currentTimeMillis(),
        colorTag = 0xFFFF00.toInt(),
        displayOption = "day"
    )
}
```

### Интеграционный тест Repository

```kotlin
@RunWith(AndroidJUnit4::class)
class ItemRepositoryIntegrationTest {

    private lateinit var repository: ItemRepository
    private lateinit var database: DaysDatabase

    @Before
    fun setup() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        database = Room.inMemoryDatabaseBuilder(
            context,
            DaysDatabase::class.java
        ).allowMainThreadQueries().build()

        repository = ItemRepositoryImpl(
            database.itemDao(),
            database.itemDao()
        )
    }

    @After
    fun tearDown() {
        database.close()
    }

    @Test
    fun insertItem_whenInserted_thenCanRetrieve() = runBlocking {
        // Given
        val item = Item(
            id = 1L,
            title = "Название",
            details = "Описание",
            timestamp = System.currentTimeMillis(),
            colorTag = 0xFFFF00.toInt(),
            displayOption = DisplayOption.DAY
        )

        // When
        val insertedId = repository.insertItem(item)
        val retrieved = repository.getItemById(insertedId)

        // Then
        assertNotNull(retrieved)
        assertEquals(item.title, retrieved!!.title)
    }

    @Test
    fun getAllItems_whenMultipleItems_thenReturnsFlow() = runBlocking {
        // Given
        val items = listOf(
            testItem(id = 1L, title = "Первый"),
            testItem(id = 2L, title = "Второй")
        )
        items.forEach { repository.insertItem(it) }

        // When
        val result = repository.getAllItems().first()

        // Then
        assertEquals(2, result.size)
        assertEquals("Первый", result[0].title)
    }
}
```

## Интеграционные тесты ViewModels (только для существующих)

⚠️ **Важно:** Создание новых интеграционных тестов ViewModels запрещено. Этот раздел только для обслуживания существующих тестов.

```kotlin
@RunWith(AndroidJUnit4::class)
@HiltAndroidTest
class DetailScreenViewModelIntegrationTest {

    @get:Rule
    val hiltRule = HiltAndroidRule(this)

    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    @get:Rule
    val mainDispatcherRule = MainDispatcherRule()

    @Inject
    lateinit var repository: ItemRepository

    private lateinit var viewModel: DetailScreenViewModel
    private lateinit var savedStateHandle: SavedStateHandle

    @Before
    fun setup() {
        hiltRule.inject()
        savedStateHandle = SavedStateHandle(mapOf("itemId" to 1L))
        viewModel = DetailScreenViewModel(repository, NoOpLogger(), savedStateHandle)
    }

    @Test
    fun whenItemExistsInDatabase_thenLoadsSuccessfully() = runTest {
        // Given
        val testItem = Item(
            id = 1L,
            title = "Тестовый элемент",
            details = "Описание",
            timestamp = System.currentTimeMillis(),
            colorTag = 0xFFFF00.toInt(),
            displayOption = DisplayOption.DAY
        )
        repository.insertItem(testItem)

        // When
        viewModel = DetailScreenViewModel(repository, NoOpLogger(), savedStateHandle)

        // Then - тестируем эмиссии StateFlow с помощью Turbine
        viewModel.uiState.test {
            val loadingState = awaitItem()
            assertTrue(loadingState is DetailScreenState.Loading)

            val successState = awaitItem()
            assertTrue(successState is DetailScreenState.Success)
            assertEquals(testItem.title, (successState as DetailScreenState.Success).item.title)
        }
    }
}
```

## UI-тесты Compose компонентов

### Простой UI-тест

```kotlin
class DaysCountTextTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun daysCountText_whenToday_thenShowsToday() {
        // Given
        val item = Item(
            id = 1L,
            title = "Тест",
            details = "Описание",
            timestamp = System.currentTimeMillis(),
            colorTag = 0xFFFF00.toInt(),
            displayOption = DisplayOption.DAY
        )

        // When
        composeTestRule.setContent {
            DaysCountText(item)
        }

        // Then
        composeTestRule.onNodeWithText("Сегодня").assertIsDisplayed()
    }

    @Test
    fun daysCountText_whenYesterday_thenShowsYesterday() {
        // Given
        val yesterday = System.currentTimeMillis() - 24 * 60 * 60 * 1000
        val item = Item(
            id = 1L,
            title = "Тест",
            details = "Описание",
            timestamp = yesterday,
            colorTag = 0xFFFF00.toInt(),
            displayOption = DisplayOption.DAY
        )

        // When
        composeTestRule.setContent {
            DaysCountText(item)
        }

        // Then
        composeTestRule.onNodeWithText("Вчера").assertIsDisplayed()
    }
}
```

### UI-тест с взаимодействием

```kotlin
class MainScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun whenAddButtonClicked_thenNavigatesToCreateScreen() {
        // Given
        val mockNavController = mockk<NavController>(relaxed = true)

        composeTestRule.setContent {
            MainScreen(
                navController = mockNavController,
                viewModel = MainScreenViewModel(mockk(relaxed = true))
            )
        }

        // When
        composeTestRule
            .onNodeWithContentDescription("Добавить")
            .performClick()

        // Then
        verify { mockNavController.navigate("create_edit") }
    }

    @Test
    fun whenItemClicked_thenNavigatesToDetailScreen() {
        // Given
        val testItem = Item(
            id = 1L,
            title = "Тестовый элемент",
            details = "Описание",
            timestamp = System.currentTimeMillis(),
            colorTag = 0xFFFF00.toInt(),
            displayOption = DisplayOption.DAY
        )
        val mockNavController = mockk<NavController>(relaxed = true)

        composeTestRule.setContent {
            MainScreen(
                navController = mockNavController,
                viewModel = MainScreenViewModel(mockk(relaxed = true))
            )
        }

        // When
        composeTestRule
            .onNodeWithText("Тестовый элемент")
            .performClick()

        // Then
        verify { mockNavController.navigate("item_detail/1") }
    }
}
```

## Тестирование Flow с исключениями

### Тестирование IOException (обрабатывается в catch)

```kotlin
class BackupExportUseCaseTest {

    private val mockRepository: ItemRepository = mockk()
    private val useCase = ExportBackupUseCase(mockRepository)

    @Test
    fun exportBackup_whenRepositoryThrowsIOException_thenReturnsFailure() = runTest {
        // Given
        val testItem = testItem()
        every { mockRepository.getAllItems() } returns flowOf(listOf(testItem))
        coEvery { mockRepository.getAllItems() } throws IOException("Нет доступа к базе данных")

        // When
        val result = useCase(Uri.parse("content://test"))

        // Then
        assertTrue(result.isFailure)
        assertTrue(result.exceptionOrNull() is BackupException)
    }
}
```

### Тестирование других исключений (пробрасываются дальше)

```kotlin
class BackupImportUseCaseTest {

    private val mockRepository: ItemRepository = mockk()
    private val useCase = ImportBackupUseCase(mockRepository)

    @Test
    fun importBackup_whenJsonInvalid_thenThrowsSerializationException() = runTest {
        // Given
        val invalidJson = "{ invalid json }"
        val uri = mockk<Uri>()

        // When & Then
        assertThrows<SerializationException> {
            useCase(uri, invalidJson)
        }
    }
}
```

### Мокирование Android Log

```kotlin
class ItemRepositoryTest {

    private val mockDao: ItemDao = mockk()
    private val mockLogger: Logger = mockk()
    private val repository = ItemRepositoryImpl(mockDao, mockDao, mockLogger)

    @Test
    fun insertItem_whenError_thenLogsError() = runTest {
        // Given
        val item = testItem()
        coEvery { mockDao.insert(any()) } throws SQLException("Ошибка базы данных")

        // When
        repository.insertItem(item)

        // Then
        verify {
            mockLogger.e(
                "ItemRepository",
                "Ошибка при вставке элемента: Ошибка базы данных"
            )
        }
    }
}
```

## Тестирование Use Cases

### Простой тест Use Case

```kotlin
class CalculateDaysDifferenceUseCaseTest {

    private val useCase = CalculateDaysDifferenceUseCase()

    @Test
    fun invoke_whenSameDay_thenReturnsZero() {
        // Given
        val date = LocalDate.now()

        // When
        val result = useCase(date, date)

        // Then
        assertEquals(0L, result.days)
    }

    @Test
    fun invoke_whenYesterday_thenReturnsOne() {
        // Given
        val today = LocalDate.now()
        val yesterday = today.minusDays(1)

        // When
        val result = useCase(yesterday, today)

        // Then
        assertEquals(1L, result.days)
    }

    @Test
    fun invoke_whenTomorrow_thenReturnsMinusOne() {
        // Given
        val today = LocalDate.now()
        val tomorrow = today.plusDays(1)

        // When
        val result = useCase(tomorrow, today)

        // Then
        assertEquals(-1L, result.days)
    }
}
```

### Тест форматирования

```kotlin
class FormatDaysTextUseCaseTest {

    private val mockResourceProvider: ResourceProvider = mockk()
    private val useCase = FormatDaysTextUseCase(mockResourceProvider)

    @Test
    fun invoke_whenZeroDays_thenReturnsToday() {
        // Given
        val daysDifference = DaysDifference(0L)
        every { mockResourceProvider.getString(R.string.today) } returns "Сегодня"

        // When
        val result = useCase(daysDifference)

        // Then
        assertEquals("Сегодня", result)
    }

    @Test
    fun invoke_whenOneDayAgo_thenReturnsYesterday() {
        // Given
        val daysDifference = DaysDifference(1L)
        every { mockResourceProvider.getString(R.string.yesterday) } returns "Вчера"

        // When
        val result = useCase(daysDifference)

        // Then
        assertEquals("Вчера", result)
    }

    @Test
    fun invoke_whenMultipleDaysAgo_thenReturnsFormattedText() {
        // Given
        val daysDifference = DaysDifference(5L)
        every {
            mockResourceProvider.getQuantityString(R.plurals.days_ago, 5, 5)
        } returns "5 дней назад"

        // When
        val result = useCase(daysDifference)

        // Then
        assertEquals("5 дней назад", result)
    }
}
```

## Параметризированные тесты

### Пример с несколькими вариантами

```kotlin
class DaysDifferenceTest {

    @ParameterizedTest
    @CsvSource(
        "0,0",
        "1,1",
        "2,2",
        "10,10",
        "365,365"
    )
    fun calculateDaysDifference_withVariousDates_returnsCorrectDays(
        daysOffset: Long,
        expectedDays: Long
    ) {
        // Given
        val fromDate = LocalDate.now().minusDays(daysOffset)
        val toDate = LocalDate.now()

        // When
        val result = DaysCalculator.calculateDaysDifference(fromDate, toDate)

        // Then
        assertEquals(expectedDays, result.days)
    }
}
```

## Тестирование резервного копирования

### Тест экспорта

```kotlin
class ExportBackupUseCaseTest {

    private val mockRepository: ItemRepository = mockk()
    private val useCase = ExportBackupUseCase(mockRepository)

    @Test
    fun invoke_whenItemsExist_thenReturnsBackupJson() = runTest {
        // Given
        val items = listOf(
            Item(
                id = 1L,
                title = "Первый",
                details = "Описание",
                timestamp = 1234567890000,
                colorTag = 0xFFFF00.toInt(),
                displayOption = DisplayOption.DAY
            )
        )
        every { mockRepository.getAllItems() } returns flowOf(items)

        // When
        val result = useCase(Uri.parse("content://test"))

        // Then
        assertTrue(result.isSuccess)
        val jsonString = result.getOrNull() ?: fail("Result should be success")
        assertTrue(jsonString.contains("Первый"))
        assertTrue(jsonString.contains("1234567890000"))
    }
}
```

### Тест импорта

```kotlin
class ImportBackupUseCaseTest {

    private val mockRepository: ItemRepository = mockk()
    private val useCase = ImportBackupUseCase(mockRepository)

    @Test
    fun invoke_whenValidJson_thenImportsItems() = runTest {
        // Given
        val jsonString = """
            [
                {
                    "title": "Импортированный",
                    "details": "Описание",
                    "timestamp": 1234567890000,
                    "colorTag": "#FFFF00",
                    "displayOption": "day"
                }
            ]
        """.trimIndent()
        val uri = mockk<Uri>()
        coEvery { mockRepository.insertItem(any()) } returns 1L

        // When
        val result = useCase(uri, jsonString)

        // Then
        assertTrue(result.isSuccess)
        coVerify { mockRepository.insertItem(any()) }
    }

    @Test
    fun invoke_whenDuplicateItem_thenSkipsDuplicate() = runTest {
        // Given
        val existingItem = Item(
            id = 1L,
            title = "Существующий",
            details = "Описание",
            timestamp = 1234567890000,
            colorTag = 0xFFFF00.toInt(),
            displayOption = DisplayOption.DAY
        )
        val jsonString = """
            [
                {
                    "title": "Существующий",
                    "details": "Описание",
                    "timestamp": 1234567890000,
                    "colorTag": "#FFFF00",
                    "displayOption": "day"
                }
            ]
        """.trimIndent()
        val uri = mockk<Uri>()
        coEvery { mockRepository.getAllItems() } returns flowOf(listOf(existingItem))
        coEvery { mockRepository.insertItem(any()) } returns 2L

        // When
        val result = useCase(uri, jsonString)

        // Then
        assertTrue(result.isSuccess)
        // Дубликат не должен быть добавлен
        coVerify(exactly = 0) { mockRepository.insertItem(any()) }
    }
}
```

## Чек-лист проверки тестов

Перед коммитом тестов:

- [ ] Все тесты проходят
- [ ] Имена тестов описательные (format: `functionName_whenCondition_thenExpectedResult`)
- [ ] Использован AAA паттерн (Arrange-Act-Assert или Given-When-Then)
- [ ] Один тест - одна проверка
- [ ] Тесты независимы друг от друга
- [ ] Тесты быстрые
- [ ] Моки настроены корректно
- [ ] Для Flow используются Turbine или `first()`
- [ ] Для исключений в Flow используется `first()` или `collect()` вместо Turbine
- [ ] Новые интеграционные тесты ViewModels не создаются (запрещено)
- [ ] Существующие интеграционные тесты ViewModels используют `runTest`, `MainDispatcherRule` и `Turbine`
