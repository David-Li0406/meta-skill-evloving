# Testing Rules

## test-compose - Write Compose UI tests correctly

Use ComposeTestRule for testing Compose UI components.

### Correct

```kotlin
class UserCardTest {
    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun userCard_displaysUserInfo() {
        val user = User(id = "1", name = "John Doe", email = "john@example.com")

        composeTestRule.setContent {
            MaterialTheme {
                UserCard(user = user)
            }
        }

        composeTestRule.onNodeWithText("John Doe").assertIsDisplayed()
        composeTestRule.onNodeWithText("john@example.com").assertIsDisplayed()
    }

    @Test
    fun userCard_callsOnClick_whenTapped() {
        var clicked = false
        val user = User(id = "1", name = "John", email = "john@example.com")

        composeTestRule.setContent {
            MaterialTheme {
                UserCard(user = user, onClick = { clicked = true })
            }
        }

        composeTestRule.onNodeWithText("John").performClick()

        assertTrue(clicked)
    }

    @Test
    fun userCard_showsLoadingState() {
        composeTestRule.setContent {
            MaterialTheme {
                UserCard(isLoading = true)
            }
        }

        composeTestRule.onNode(hasProgressBarRangeInfo(ProgressBarRangeInfo.Indeterminate))
            .assertIsDisplayed()
    }

    @Test
    fun userList_scrollsToItem() {
        val users = (1..100).map { User("$it", "User $it", "user$it@example.com") }

        composeTestRule.setContent {
            UserList(users = users)
        }

        composeTestRule.onNodeWithText("User 50").assertDoesNotExist()

        composeTestRule.onNodeWithTag("user_list")
            .performScrollToIndex(49)

        composeTestRule.onNodeWithText("User 50").assertIsDisplayed()
    }
}
```

---

## test-coroutine - Test coroutines with TestDispatcher

Use TestDispatcher for deterministic coroutine testing.

### Correct

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class UserViewModelTest {
    private val testDispatcher = StandardTestDispatcher()
    private lateinit var viewModel: UserViewModel
    private lateinit var repository: FakeUserRepository

    @BeforeTest
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        repository = FakeUserRepository()
        viewModel = UserViewModel(repository)
    }

    @AfterTest
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun loadUser_emitsLoadingThenSuccess() = runTest {
        val user = User("1", "John")
        repository.setUser(user)

        val states = mutableListOf<UserUiState>()
        val job = launch(UnconfinedTestDispatcher(testScheduler)) {
            viewModel.state.toList(states)
        }

        viewModel.loadUser("1")
        advanceUntilIdle()

        assertEquals(
            listOf(UserUiState.Loading, UserUiState.Success(user)),
            states.drop(1) // Skip initial state
        )

        job.cancel()
    }

    @Test
    fun loadUser_emitsError_onFailure() = runTest {
        repository.setShouldFail(true)

        viewModel.loadUser("1")
        advanceUntilIdle()

        assertTrue(viewModel.state.value is UserUiState.Error)
    }

    @Test
    fun loadUser_cancelsOnNewRequest() = runTest {
        val user1 = User("1", "John")
        val user2 = User("2", "Jane")
        repository.setUsers(mapOf("1" to user1, "2" to user2))
        repository.setDelay(1000)

        viewModel.loadUser("1")
        advanceTimeBy(500) // Halfway through first request
        viewModel.loadUser("2") // Cancel first, start second
        advanceUntilIdle()

        val state = viewModel.state.value
        assertTrue(state is UserUiState.Success)
        assertEquals(user2, (state as UserUiState.Success).user)
    }
}
```

---

## test-flow - Test Flow emissions with Turbine

Use Turbine library for testing Flow emissions.

### Correct

```kotlin
class UserRepositoryTest {
    @Test
    fun observeUsers_emitsUpdates() = runTest {
        val repository = UserRepositoryImpl(fakeDatabase)

        repository.observeUsers().test {
            // Initial empty state
            assertEquals(emptyList<User>(), awaitItem())

            // Add user
            repository.addUser(User("1", "John"))
            assertEquals(listOf(User("1", "John")), awaitItem())

            // Add another user
            repository.addUser(User("2", "Jane"))
            assertEquals(
                listOf(User("1", "John"), User("2", "Jane")),
                awaitItem()
            )

            cancelAndConsumeRemainingEvents()
        }
    }

    @Test
    fun observeUser_completesOnDeletion() = runTest {
        val repository = UserRepositoryImpl(fakeDatabase)
        repository.addUser(User("1", "John"))

        repository.observeUser("1").test {
            assertEquals(User("1", "John"), awaitItem())

            repository.deleteUser("1")

            awaitComplete()
        }
    }

    @Test
    fun searchUsers_debounces() = runTest {
        repository.searchUsers("J").test {
            // Should debounce rapid queries
            repository.updateQuery("Jo")
            repository.updateQuery("Joh")
            repository.updateQuery("John")

            // Only final result emitted after debounce
            val results = awaitItem()
            assertTrue(results.all { it.name.startsWith("John") })

            cancelAndConsumeRemainingEvents()
        }
    }
}
```

---

## test-koin - Setup Koin for testing

Configure Koin properly for unit and integration tests.

### Correct

```kotlin
class UserViewModelKoinTest : KoinTest {
    private val mockRepository: UserRepository = mockk()

    @get:Rule
    val koinTestRule = KoinTestRule.create {
        modules(
            module {
                single<UserRepository> { mockRepository }
                viewModel { UserViewModel(get()) }
            }
        )
    }

    private val viewModel: UserViewModel by inject()

    @Test
    fun loadUser_callsRepository() = runTest {
        val user = User("1", "John")
        coEvery { mockRepository.getUser("1") } returns Result.success(user)

        viewModel.loadUser("1")

        coVerify { mockRepository.getUser("1") }
    }
}

// Without Rule, manual start/stop
class ManualKoinTest : KoinTest {
    @BeforeTest
    fun setup() {
        startKoin {
            modules(testModule)
        }
    }

    @AfterTest
    fun tearDown() {
        stopKoin()
    }
}

// Compose integration test with Koin
class UserScreenKoinTest {
    @get:Rule
    val composeTestRule = createComposeRule()

    @get:Rule
    val koinTestRule = KoinTestRule.create {
        modules(testModule)
    }

    @Test
    fun userScreen_loadsAndDisplaysUser() {
        composeTestRule.setContent {
            KoinContext {
                UserScreen(userId = "1")
            }
        }

        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithText("John Doe").assertIsDisplayed()
    }
}
```

---

## test-ktor - Mock Ktor client responses

Use MockEngine for testing Ktor client code.

### Correct

```kotlin
class UserApiTest {
    @Test
    fun getUser_parsesResponse() = runTest {
        val mockEngine = MockEngine { request ->
            when {
                request.url.encodedPath == "/users/1" -> respond(
                    content = ByteReadChannel("""{"id":"1","name":"John","email":"john@example.com"}"""),
                    status = HttpStatusCode.OK,
                    headers = headersOf(HttpHeaders.ContentType, "application/json")
                )
                else -> respond(
                    content = ByteReadChannel(""),
                    status = HttpStatusCode.NotFound
                )
            }
        }

        val client = HttpClient(mockEngine) {
            install(ContentNegotiation) { json() }
        }

        val api = UserApi(client)
        val result = api.getUser("1")

        assertEquals(User("1", "John", "john@example.com"), result)
    }

    @Test
    fun getUser_handlesError() = runTest {
        val mockEngine = MockEngine {
            respond(
                content = ByteReadChannel("""{"error":"User not found"}"""),
                status = HttpStatusCode.NotFound
            )
        }

        val client = HttpClient(mockEngine) {
            install(ContentNegotiation) { json() }
        }

        val api = UserApi(client)

        assertFailsWith<ClientRequestException> {
            api.getUser("999")
        }
    }

    @Test
    fun createUser_sendsCorrectBody() = runTest {
        var capturedBody: String? = null

        val mockEngine = MockEngine { request ->
            capturedBody = request.body.toByteArray().decodeToString()
            respond(
                content = ByteReadChannel("""{"id":"1","name":"John","email":"john@example.com"}"""),
                status = HttpStatusCode.Created,
                headers = headersOf(HttpHeaders.ContentType, "application/json")
            )
        }

        val client = HttpClient(mockEngine) {
            install(ContentNegotiation) { json() }
        }

        val api = UserApi(client)
        api.createUser("John", "john@example.com")

        assertNotNull(capturedBody)
        assertTrue(capturedBody!!.contains("John"))
        assertTrue(capturedBody!!.contains("john@example.com"))
    }
}
```

---

## test-snapshot - Use screenshot tests for UI

Capture and compare screenshots for visual regression.

### Correct

```kotlin
class UserCardScreenshotTest {
    @get:Rule
    val composeTestRule = createComposeRule()

    @Test
    fun userCard_matchesDesign() {
        val user = User("1", "John Doe", "john@example.com")

        composeTestRule.setContent {
            MaterialTheme {
                UserCard(user = user)
            }
        }

        composeTestRule.onRoot().captureToImage()
            .assertAgainstGolden(goldenPath = "user_card_default")
    }

    @Test
    fun userCard_loadingState_matchesDesign() {
        composeTestRule.setContent {
            MaterialTheme {
                UserCard(isLoading = true)
            }
        }

        composeTestRule.onRoot().captureToImage()
            .assertAgainstGolden(goldenPath = "user_card_loading")
    }

    @Test
    fun userCard_darkTheme_matchesDesign() {
        val user = User("1", "John Doe", "john@example.com")

        composeTestRule.setContent {
            MaterialTheme(colorScheme = darkColorScheme()) {
                UserCard(user = user)
            }
        }

        composeTestRule.onRoot().captureToImage()
            .assertAgainstGolden(goldenPath = "user_card_dark")
    }
}
```
