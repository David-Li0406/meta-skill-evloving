using System.Data;
using System.Data.Odbc;
using Microsoft.Extensions.Logging;
namespace ServiceLib
{
    /// <summary>
    /// A platform-agnostic ODBC connection handler that works with various database systems 
    /// including MS SQL Server, PostgreSQL, DuckDB and others via ODBC drivers.
    /// </summary>
    public class ODBC : IDisposable
    {
        private readonly string _connectionString;
        private readonly OdbcConnection _connection;
        protected readonly ILogger _logger;

        public ODBC(string connectionString, ILogger logger)
        {
            _connectionString = connectionString;
            _connection = new OdbcConnection(_connectionString);
            _logger = logger;
        }

        public void Open()
        {
            _connection.Open();
        }

        public void Close()
        {
            _connection.Close();
        }

        /// <summary>
        /// Executes a SQL query and returns the results as a DataTable.
        /// </summary>
        /// <param name="sqlQuery">The SQL query to execute</param>
        /// <param name="parameters">Optional list of parameter values in the order they appear in the query.
        /// Each ? in the query will be replaced by the corresponding parameter in the list.</param>
        /// <returns>A DataTable containing the query results</returns>
        public DataTable ExecuteQuery(string sqlQuery, List<object>? parameters = null)
        {
            using var command = new OdbcCommand(sqlQuery, _connection);
            if (parameters != null)
            {
                foreach (var param in parameters)
                {
                    command.Parameters.Add(new OdbcParameter("?", param));
                }
            }

            var dataTable = new DataTable();
            using (var adapter = new OdbcDataAdapter(command))
            {
                adapter.Fill(dataTable);
            }
            return dataTable;
        }

        /// <summary>
        /// Executes a SQL query and returns the results as a DataTable.
        /// </summary>
        /// <param name="sqlQuery">The SQL query to execute</param>
        /// <param name="parameters">Optional dictionary of parameters - kept for backward compatibility</param>
        /// <returns>A DataTable containing the query results</returns>
        public DataTable ExecuteQuery(string sqlQuery, Dictionary<string, object>? parameters = null)
        {
            if (parameters == null)
            {
                return ExecuteQuery(sqlQuery, (List<object>?)null);
            }
            
            // Convert dictionary to list for positional parameters
            var paramsList = parameters.Values.ToList();
            return ExecuteQuery(sqlQuery, paramsList);
        }

        /// <summary>
        /// Asynchronously executes a SQL query and returns the results as a DataTable.
        /// </summary>
        /// <param name="sqlQuery">The SQL query to execute</param>
        /// <param name="parameters">Optional dictionary of parameters to protect against SQL injection</param>
        /// <returns>A Task containing a DataTable with the query results</returns>
        public async Task<DataTable> ExecuteQueryAsync(string sqlQuery, Dictionary<string, object>? parameters = null)
        {
            using var command = new OdbcCommand(sqlQuery, _connection);
            if (parameters != null)
            {
                foreach (var param in parameters)
                {
                    command.Parameters.AddWithValue(param.Key, param.Value);
                }
            }

            var dataTable = new DataTable();
            using (var adapter = new OdbcDataAdapter(command))
            {
                await Task.Run(() => adapter.Fill(dataTable));
            }
            return dataTable;
        }

        /// <summary>
        /// Executes a SQL command that doesn't return results (INSERT, UPDATE, DELETE, etc).
        /// </summary>
        /// <param name="sqlCommand">The SQL command to execute</param>
        /// <param name="parameters">Optional dictionary of parameters to protect against SQL injection</param>
        /// <returns>The number of rows affected by the command</returns>
        public int ExecuteNonQuery(string sqlCommand, Dictionary<string, object>? parameters = null)
        {
            using var command = new OdbcCommand(sqlCommand, _connection);
            if (parameters != null)
            {
                foreach (var param in parameters)
                {
                    command.Parameters.AddWithValue(param.Key, param.Value);
                }
            }
            return command.ExecuteNonQuery();
        }

        /// <summary>
        /// Asynchronously executes a SQL command that doesn't return results (INSERT, UPDATE, DELETE, etc).
        /// </summary>
        /// <param name="sqlCommand">The SQL command to execute</param>
        /// <param name="parameters">Optional dictionary of parameters to protect against SQL injection</param>
        /// <returns>A Task containing the number of rows affected by the command</returns>
        public async Task<int> ExecuteNonQueryAsync(string sqlCommand, Dictionary<string, object>? parameters = null)
        {
            using var command = new OdbcCommand(sqlCommand, _connection);
            if (parameters != null)
            {
                foreach (var param in parameters)
                {
                    command.Parameters.AddWithValue(param.Key, param.Value);
                }
            }
            return await command.ExecuteNonQueryAsync();
        }

        /// <summary>
        /// Executes a SQL query and returns a single value of the specified type.
        /// </summary>
        /// <typeparam name="T">The expected type of the returned value</typeparam>
        /// <param name="sqlQuery">The SQL query to execute</param>
        /// <param name="parameters">Optional dictionary of parameters to protect against SQL injection</param>
        /// <returns>The first column of the first row in the result set, or default(T) if the result set is empty</returns>
        public T? ExecuteScalar<T>(string sqlQuery, Dictionary<string, object>? parameters = null)
        {
            using var command = new OdbcCommand(sqlQuery, _connection);
            if (parameters != null)
            {
                foreach (var param in parameters)
                {
                    command.Parameters.AddWithValue(param.Key, param.Value);
                }
            }
            var result = command.ExecuteScalar();
            return result == DBNull.Value ? default(T) : (T?)result;
        }

        /// <summary>
        /// Asynchronously executes a SQL query and returns a single value of the specified type.
        /// </summary>
        /// <typeparam name="T">The expected type of the returned value</typeparam>
        /// <param name="sqlQuery">The SQL query to execute</param>
        /// <param name="parameters">Optional dictionary of parameters to protect against SQL injection</param>
        /// <returns>A Task containing the first column of the first row in the result set, or default(T) if the result set is empty</returns>
        public async Task<T?> ExecuteScalarAsync<T>(string sqlQuery, Dictionary<string, object>? parameters = null)
        {
            using var command = new OdbcCommand(sqlQuery, _connection);
            if (parameters != null)
            {
                foreach (var param in parameters)
                {
                    command.Parameters.AddWithValue(param.Key, param.Value);
                }
            }
            var result = await command.ExecuteScalarAsync();
            return result == DBNull.Value ? default : (T?)result;
        }

        public async Task<OdbcDataReader> ExecuteReaderAsync(string sqlQuery, Dictionary<string, object>? parameters = null)
        {
            var command = new OdbcCommand(sqlQuery, _connection);
            if (parameters != null)
            {
                foreach (var param in parameters)
                {
                    command.Parameters.AddWithValue(param.Key, param.Value);
                }
            }
            return (OdbcDataReader)await command.ExecuteReaderAsync();
        }

        public OdbcDataReader ExecuteReader(string sqlQuery, Dictionary<string, object>? parameters = null)
        {
            var command = new OdbcCommand(sqlQuery, _connection);
            if (parameters != null)
            {
                foreach (var param in parameters)
                {
                    command.Parameters.AddWithValue(param.Key, param.Value);
                }
            }
            
            _logger.LogDebug("Running command: {0}", GetCommandText(command));
            return command.ExecuteReader();
        }

        public static string GetCommandText(OdbcCommand command)
        {
            string commandText = command.CommandText;
            
            // If there are no parameters or no '?' in the command, return as is
            if (command.Parameters.Count == 0 || !commandText.Contains('?'))
                return commandText;
            
            // Create a list of parameter values in the proper format for substitution
            var paramValues = new List<string>();
            foreach (OdbcParameter parameter in command.Parameters)
            {
                string parameterValue;
                
                if (parameter.Value == null)
                {
                    parameterValue = "NULL";
                }
                else if (parameter.Value is string s)
                {
                    // Just escape quotes without additional encoding 
                    // that might be corrupting UTF-8 characters
                    parameterValue = $"'{s.Replace("'", "''")}'";
                }
                else if (parameter.Value is DateTime dt)
                {
                    parameterValue = $"'{dt:yyyy-MM-dd HH:mm:ss}'";
                }
                else if (parameter.Value is bool b)
                {
                    parameterValue = b ? "1" : "0";
                }
                else
                {
                    parameterValue = parameter.Value.ToString() ?? "NULL";
                }
                
                paramValues.Add(parameterValue);
            }
            
            // Replace each '?' with the corresponding parameter value
            for (int i = 0; i < paramValues.Count; i++)
            {
                int pos = commandText.IndexOf('?');
                if (pos >= 0)
                {
                    commandText = commandText.Substring(0, pos) + paramValues[i] + commandText.Substring(pos + 1);
                }
            }
            
            return commandText;
        }
        /// <summary>
        /// Creates a PostgreSQL ARRAY literal from a list of strings, properly escaped.
        /// </summary>
        /// <param name="values">The string values to include in the array</param>
        /// <returns>A properly formatted and escaped PostgreSQL ARRAY literal</returns>
        public static string CreatePostgresArrayLiteral(IEnumerable<string> values)
        {
            // Escape each value and wrap in single quotes
            var escapedValues = values.Select(v => "'" + v.Replace("'", "''") + "'");
            return $"ARRAY[{string.Join(", ", escapedValues)}]";
        }

        /// <summary>
        /// Creates a PostgreSQL ARRAY literal from a list of integers.
        /// </summary>
        /// <param name="values">The integer values to include in the array</param>
        /// <returns>A properly formatted PostgreSQL ARRAY literal</returns>
        public static string CreatePostgresArrayLiteral(IEnumerable<int> values)
        {
            return $"ARRAY[{string.Join(", ", values)}]";
        }

        /// <summary>
        /// Creates a PostgreSQL ARRAY literal from a list of objects, determining the appropriate format based on type.
        /// </summary>
        /// <param name="values">The values to include in the array</param>
        /// <returns>A properly formatted PostgreSQL ARRAY literal</returns>
        public static string CreatePostgresArrayLiteral(IEnumerable<object> values)
        {
            var formattedValues = values.Select(v => 
            {
                if (v is string s)
                    return "'" + s.Replace("'", "''") + "'";
                else if (v is DateTime dt)
                    return $"'{dt:yyyy-MM-dd HH:mm:ss}'";
                else if (v is bool b)
                    return b ? "true" : "false";
                else
                    return v.ToString();
            });
            
            return $"ARRAY[{string.Join(", ", formattedValues)}]";
        }

        /// <summary>
        /// Prepares a PostgreSQL query by replacing parameter placeholders with proper values.
        /// This is particularly useful for handling arrays with ANY() which cannot be bound as regular parameters.
        /// </summary>
        /// <param name="sqlQuery">The SQL query with ? placeholders</param>
        /// <param name="parameters">Dictionary of parameters. Array parameters will be formatted as PostgreSQL arrays.</param>
        /// <returns>SQL query with parameter values properly substituted and escaped</returns>
        public static string PreparePostgresQuery(string sqlQuery, Dictionary<string, object> parameters)
        {
            // Count the number of ? placeholders
            int paramCount = sqlQuery.Count(c => c == '?');
            
            if (paramCount != parameters.Count)
            {
                throw new ArgumentException($"Parameter count mismatch: {paramCount} placeholders but {parameters.Count} parameters provided");
            }
            
            string result = sqlQuery;
            foreach (var param in parameters)
            {
                string paramValue;
                
                // Handle different parameter types
                if (param.Value is IEnumerable<string> stringArray)
                {
                    // For string arrays, create a proper PostgreSQL array literal
                    paramValue = CreatePostgresArrayLiteral(stringArray);
                }
                else if (param.Value is IEnumerable<int> intArray)
                {
                    // For integer arrays, create a proper PostgreSQL array literal
                    paramValue = CreatePostgresArrayLiteral(intArray);
                }
                else if (param.Value is Array objArray)
                {
                    // For general arrays, convert to IEnumerable<object>
                    paramValue = CreatePostgresArrayLiteral(objArray.Cast<object>());
                }
                else if (param.Value is string s)
                {
                    // Escape single quotes and wrap in single quotes
                    paramValue = "'" + s.Replace("'", "''") + "'";
                }
                else if (param.Value is DateTime dt)
                {
                    // Format date/time and wrap in single quotes
                    paramValue = $"'{dt:yyyy-MM-dd HH:mm:ss}'";
                }
                else if (param.Value is bool b)
                {
                    // Convert boolean to PostgreSQL boolean literal
                    paramValue = b ? "true" : "false";
                }
                else if (param.Value is null)
                {
                    // Handle null values
                    paramValue = "NULL";
                }
                else
                {
                    // For other types, use string representation
                    paramValue = param.Value?.ToString() ?? "NULL";
                }
                
                // Replace the first occurrence of ? with the parameter value
                int pos = result.IndexOf('?');
                if (pos >= 0)
                {
                    result = result.Substring(0, pos) + paramValue + result.Substring(pos + 1);
                }
            }
            
            return result;
        }

        /// <summary>
        /// Executes a PostgreSQL query with proper handling of array parameters.
        /// </summary>
        /// <param name="sqlQuery">The SQL query with ? placeholders</param>
        /// <param name="parameters">Dictionary of parameters. Array parameters will be formatted as PostgreSQL arrays.</param>
        /// <returns>A DataTable containing the query results</returns>
        public DataTable ExecutePostgresQuery(string sqlQuery, Dictionary<string, object> parameters)
        {
            string preparedQuery = PreparePostgresQuery(sqlQuery, parameters);
            return ExecuteQuery(preparedQuery, new List<object>());
        }

        public void Dispose()
        {
            // Dispose of unmanaged resources.
            Dispose(true);
            // Suppress finalization.
            GC.SuppressFinalize(this);
        }

        protected virtual void Dispose(bool disposing)
        {
            if (disposing)
            {
                // Dispose managed resources
                _connection?.Dispose();
            }
        }

        /// <summary>
        /// Executes an SQL query and maps the results using the provided mapping function.
        /// This version maps each row to a single object (one-to-one).
        /// </summary>
        /// <typeparam name="TResult">The type of objects to return</typeparam>
        /// <param name="query">The SQL query to execute</param>
        /// <param name="parameters">Optional dictionary of parameters for the query</param>
        /// <param name="mapper">A function that maps an IDataReader row to a single object</param>
        /// <returns>A list of mapped objects</returns>
        public List<TResult> ExecuteAndMap<TResult>(
            string query,
            Dictionary<string, object>? parameters,
            Func<IDataReader, TResult> mapper
        )
        {
            var results = new List<TResult>();
            Open();
            using var reader = ExecuteReader(query, parameters);
            while (reader.Read())
            {
                results.Add(mapper(reader));
            }
            Close();
            return results;
        }

        private bool InsertDataByRow(string table, DataTable data)
        {
            var columns = string.Join(", ", data.Columns.Cast<DataColumn>().Select(c => $"\"{c.ColumnName}\""));
            var success = true;
            
            Open();
            foreach (DataRow row in data.Rows)
            {
                var values = row.ItemArray.Select(value => 
                {
                    if (value == null || value == DBNull.Value)
                        return "NULL";
                        
                    return value switch
                    {
                        string s => $"'{s.Replace("'", "''")}'",
                        int or long or float or double or decimal => value.ToString(),
                        bool b => b ? "1" : "0",
                        DateTime dt => dt.TimeOfDay.Ticks == 0 
                            ? $"'{dt:yyyy-MM-dd}'" 
                            : $"'{dt:yyyy-MM-dd HH:mm:ss}'",
                        _ => $"'{value.ToString()?.Replace("'", "''")}'"
                    };
                });
                
                var query = $"INSERT INTO [{table}] ({columns}) VALUES ({string.Join(", ", values)})";
                _logger.LogDebug("Inserting row into {0}: {1}", table, query);
                
                if (ExecuteNonQuery(query) <= 0)
                {
                    success = false;
                    break;
                }
            }
            Close();
            return success;
        }

        private bool InsertDataMultiValues(string table, DataTable data)
        {
            var columns = string.Join(", ", data.Columns.Cast<DataColumn>().Select(c => $"\"{c.ColumnName}\""));
            var rowValues = data.AsEnumerable().Select(row => 
            {
                var values = row.ItemArray.Select(value => 
                {
                    if (value == null || value == DBNull.Value)
                        return "NULL";
                        
                    return value switch
                    {
                        string s => $"'{s.Replace("'", "''")}'",
                        int or long or float or double or decimal => value.ToString(),
                        bool b => b ? "1" : "0",
                        DateTime dt => dt.TimeOfDay.Ticks == 0 
                            ? $"'{dt:yyyy-MM-dd}'" 
                            : $"'{dt:yyyy-MM-dd HH:mm:ss}'",
                        _ => $"'{value.ToString()?.Replace("'", "''")}'"
                    };
                });
                return $"({string.Join(", ", values)})";
            });
            
            var query = $"INSERT INTO [{table}] ({columns}) VALUES {string.Join(", ", rowValues)}";
            _logger.LogDebug("Inserting data into {0}: {1}", table, query);
            Open();
            var result = ExecuteNonQuery(query) > 0;
            Close();
            return result;
        }

        public bool InsertData(string table, DataTable data)
        {
            try
            {
                // Try multi-row insert first
                return InsertDataMultiValues(table, data);
            }
            catch (OdbcException)
            {
                _logger.LogWarning("Multi-row insert failed, falling back to row-by-row insert");
                // Ensure connection is closed before trying row-by-row
                try { Close(); } catch { }
                // If multi-row fails, fall back to row-by-row
                return InsertDataByRow(table, data);
            }
        }
    }
}
