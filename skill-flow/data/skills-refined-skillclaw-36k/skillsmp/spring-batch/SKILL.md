---
name: Spring Batch
description: Job configuration, chunk processing, readers, writers, processors, and job execution.
metadata:
  labels: [java, spring-boot, batch, etl]
  triggers:
    files: ['**/*Batch*.java', '**/*Job*.java', '**/*Step*.java']
    keywords: [Job, Step, ItemReader, ItemWriter, ItemProcessor, JobBuilder, StepBuilder, Chunk, Tasklet]
---

# Spring Batch Standards

## Job Configuration

```java
@Configuration
@RequiredArgsConstructor
public class UserExportJobConfig {

    private final JobRepository jobRepository;
    private final PlatformTransactionManager transactionManager;

    @Bean
    public Job userExportJob(Step exportStep) {
        return new JobBuilder("userExportJob", jobRepository)
            .incrementer(new RunIdIncrementer())
            .start(exportStep)
            .build();
    }

    @Bean
    public Step exportStep(
            ItemReader<User> reader,
            ItemProcessor<User, UserDto> processor,
            ItemWriter<UserDto> writer) {
        return new StepBuilder("exportStep", jobRepository)
            .<User, UserDto>chunk(100, transactionManager)
            .reader(reader)
            .processor(processor)
            .writer(writer)
            .faultTolerant()
            .skipLimit(10)
            .skip(DataAccessException.class)
            .build();
    }
}
```

## Reader/Processor/Writer

```java
@Bean
public JpaPagingItemReader<User> userReader(EntityManagerFactory emf) {
    return new JpaPagingItemReaderBuilder<User>()
        .name("userReader")
        .entityManagerFactory(emf)
        .queryString("SELECT u FROM User u WHERE u.status = 'ACTIVE'")
        .pageSize(100)
        .build();
}

@Bean
public ItemProcessor<User, UserDto> userProcessor() {
    return user -> new UserDto(user.getId(), user.getName(), user.getEmail());
}

@Bean
public FlatFileItemWriter<UserDto> userWriter() {
    return new FlatFileItemWriterBuilder<UserDto>()
        .name("userWriter")
        .resource(new FileSystemResource("output/users.csv"))
        .delimited()
        .names("id", "name", "email")
        .build();
}
```

## Job Execution

```java
@Service
@RequiredArgsConstructor
public class JobLauncherService {

    private final JobLauncher jobLauncher;
    private final Job userExportJob;

    public void runExport(String date) throws Exception {
        JobParameters params = new JobParametersBuilder()
            .addString("date", date)
            .addLong("time", System.currentTimeMillis())
            .toJobParameters();

        JobExecution execution = jobLauncher.run(userExportJob, params);
        log.info("Job status: {}", execution.getStatus());
    }
}
```

## References

- [Chunk Processing](references/chunk-processing.md) - Sizing, transactions, error handling
