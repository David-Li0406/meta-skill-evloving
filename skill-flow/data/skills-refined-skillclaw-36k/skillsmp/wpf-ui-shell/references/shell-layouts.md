# Shell Layouts

## Standard shell

Use a simple two-row grid with a top bar and content host.

```xml
<Grid>
  <Grid.RowDefinitions>
    <RowDefinition Height="Auto" />
    <RowDefinition Height="*" />
  </Grid.RowDefinitions>

  <DockPanel Grid.Row="0">
    <!-- App title, primary nav -->
  </DockPanel>

  <ContentControl Grid.Row="1"
                  Content="{Binding CurrentViewModel}" />
</Grid>
```

## Shell with left rail

Add a left column for primary navigation while keeping a single content host.

```xml
<Grid>
  <Grid.ColumnDefinitions>
    <ColumnDefinition Width="Auto" />
    <ColumnDefinition Width="*" />
  </Grid.ColumnDefinitions>

  <StackPanel Grid.Column="0">
    <!-- Nav rail -->
  </StackPanel>

  <ContentControl Grid.Column="1"
                  Content="{Binding CurrentViewModel}" />
</Grid>
```

## Notes

- Keep layout containers shallow to reduce visual tree depth.
- Avoid Frame navigation; use ContentControl + DataTemplates instead.
