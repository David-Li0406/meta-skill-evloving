using Npgsql;
using System;
using System.IO;

if (args.Length == 0)
{
    Console.WriteLine("Usage:");
    Console.WriteLine("  PgQuery \"YOUR SQL QUERY\"");
    Console.WriteLine("  PgQuery -f script.sql");
    Console.WriteLine("  PgQuery -f script.sql -o output.txt");
    return;
}

string sql;
string? outputFile = null;

// Parse arguments
if (args[0] == "-f" && args.Length >= 2)
{
    // Read SQL from file
    var sqlFile = args[1];
    if (!File.Exists(sqlFile))
    {
        Console.WriteLine($"Error: File not found: {sqlFile}");
        return;
    }
    sql = File.ReadAllText(sqlFile);

    // Check for output file
    if (args.Length >= 4 && args[2] == "-o")
    {
        outputFile = args[3];
    }
}
else
{
    // Use SQL from command line
    sql = args[0];

    // Check for output file
    if (args.Length >= 3 && args[1] == "-o")
    {
        outputFile = args[2];
    }
}

var connString = "Host=rivsprod01;Database=x3rocs;Username=jordan";

try
{
    using var conn = new NpgsqlConnection(connString);
    conn.Open();

    using var cmd = new NpgsqlCommand(sql, conn);

    // Execute and check if there's a result set
    using var reader = cmd.ExecuteReader();

    if (reader.FieldCount == 0)
    {
        Console.WriteLine("(0 rows)");
        return;
    }

    StreamWriter? writer = null;
    if (outputFile != null)
    {
        writer = new StreamWriter(outputFile);
    }

    // Print column headers
    for (int i = 0; i < reader.FieldCount; i++)
    {
        var header = reader.GetName(i).PadRight(25);
        Console.Write(header);
        writer?.Write(header);
    }
    Console.WriteLine();
    writer?.WriteLine();

    var separator = new string('-', reader.FieldCount * 25);
    Console.WriteLine(separator);
    writer?.WriteLine(separator);

    // Print rows
    int rowCount = 0;
    while (reader.Read())
    {
        for (int i = 0; i < reader.FieldCount; i++)
        {
            var value = reader.IsDBNull(i) ? "NULL" : reader.GetValue(i).ToString();
            var formatted = (value ?? "NULL").PadRight(25);
            Console.Write(formatted);
            writer?.Write(formatted);
        }
        Console.WriteLine();
        writer?.WriteLine();
        rowCount++;
    }

    Console.WriteLine($"\n({rowCount} rows)");
    writer?.WriteLine($"\n({rowCount} rows)");

    writer?.Close();

    if (outputFile != null)
    {
        Console.WriteLine($"Output written to: {outputFile}");
    }
}
catch (Exception ex)
{
    Console.WriteLine($"Error: {ex.Message}");
}
