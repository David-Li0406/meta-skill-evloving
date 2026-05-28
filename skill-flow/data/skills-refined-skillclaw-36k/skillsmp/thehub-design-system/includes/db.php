<?php
/**
 * Database Connection Handler
 * Provides secure PDO connection and helper functions
 * Falls back to demo mode if database config doesn't exist
 */

// Try to load database configuration if it exists
$db_config_file = __DIR__ . '/../config/database.php';
if (file_exists($db_config_file)) {
    require_once $db_config_file;
}

// Check if constants are defined (from config.php via .env or config/database.php)
// If not, use fallback demo mode
if (!defined('DB_HOST')) {
    define('DB_HOST', 'localhost');
    define('DB_NAME', 'thehub_demo');
    define('DB_USER', 'demo');
    define('DB_PASS', 'demo');
    define('DB_CHARSET', 'utf8mb4');
    define('DB_ERROR_DISPLAY', false);
}

class Database {
    private static $instance = null;
    private $conn;

    private function __construct() {
        // In demo mode, don't connect to database
        if (DB_NAME === 'thehub_demo') {
            error_log("🚨 DEMO MODE ACTIVE - NO DATA WILL BE SAVED!");
            error_log("   Create config/database.php or .env file with real database credentials");
            $this->conn = null;
            return;
        }

        try {
            $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET;
            $options = [
                PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES   => false,
                PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES " . DB_CHARSET
            ];

            $this->conn = new PDO($dsn, DB_USER, DB_PASS, $options);
            error_log("✅ Database connected successfully");
            error_log("   Host: " . DB_HOST . " | Database: " . DB_NAME);
        } catch(PDOException $e) {
            // Database connection failed
            error_log("🚨 DATABASE CONNECTION FAILED!");
            error_log("   Error: " . $e->getMessage());
            error_log("   Host: " . DB_HOST . " | Database: " . DB_NAME . " | User: " . DB_USER);
            error_log("   ⚠️  ALL DATABASE OPERATIONS WILL FAIL!");
            $this->conn = null;
        }
    }

    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    public function getConnection() {
        return $this->conn;
    }

    /**
     * Execute a query and return results
     */
    public function query($sql, $params = []) {
        // Demo mode - return false
        if ($this->conn === null) {
            return false;
        }

        try {
            $stmt = $this->conn->prepare($sql);
            $stmt->execute($params);
            return $stmt;
        } catch(PDOException $e) {
            error_log("Query failed: " . $e->getMessage() . " | SQL: " . $sql);
            return false;
        }
    }

    /**
     * Get single row
     */
    public function getRow($sql, $params = []) {
        // Demo mode - return empty array
        if ($this->conn === null) {
            return [];
        }

        $stmt = $this->query($sql, $params);
        if (!$stmt) return [];
        return $stmt->fetch() ?: [];
    }

    /**
     * Get all rows
     */
    public function getAll($sql, $params = []) {
        // Demo mode - return empty array
        if ($this->conn === null) {
            return [];
        }

        $stmt = $this->query($sql, $params);
        if (!$stmt) return [];
        return $stmt->fetchAll();
    }

    /**
     * Insert and return last insert ID
     */
    public function insert($table, $data) {
        // Demo mode - return 0
        if ($this->conn === null) {
            error_log("🚨 INSERT FAILED: No database connection (demo mode or connection error)");
            error_log("   Table: {$table}");
            error_log("   Data: " . json_encode($data));
            return 0;
        }

        $fields = array_keys($data);
        $values = array_values($data);
        $placeholders = array_fill(0, count($fields), '?');

        $sql = "INSERT INTO {$table} (" . implode(', ', $fields) . ")
                VALUES (" . implode(', ', $placeholders) . ")";

        $stmt = $this->query($sql, $values);
        if (!$stmt) {
            error_log("🚨 INSERT QUERY FAILED for table: {$table}");
            return 0;
        }

        $insertId = $this->conn->lastInsertId();
        error_log("✅ INSERT successful in {$table}, ID: {$insertId}");
        return $insertId;
    }

    /**
     * Update records
     */
    public function update($table, $data, $where, $whereParams = []) {
        // Demo mode - return 0
        if ($this->conn === null) {
            return 0;
        }

        $fields = [];
        foreach (array_keys($data) as $field) {
            $fields[] = "{$field} = ?";
        }

        $sql = "UPDATE {$table} SET " . implode(', ', $fields) . " WHERE {$where}";
        $params = array_merge(array_values($data), $whereParams);

        $stmt = $this->query($sql, $params);
        if (!$stmt) return 0;
        return $stmt->rowCount();
    }

    /**
     * Delete records
     */
    public function delete($table, $where, $params = []) {
        // Demo mode - return 0
        if ($this->conn === null) {
            return 0;
        }

        $sql = "DELETE FROM {$table} WHERE {$where}";
        $stmt = $this->query($sql, $params);
        if (!$stmt) return 0;
        return $stmt->rowCount();
    }

    /**
     * Begin transaction
     */
    public function beginTransaction() {
        return $this->conn->beginTransaction();
    }

    /**
     * Commit transaction
     */
    public function commit() {
        return $this->conn->commit();
    }

    /**
     * Rollback transaction
     */
    public function rollback() {
        return $this->conn->rollBack();
    }
}

/**
 * Get database instance
 */
function getDB() {
    return Database::getInstance();
}
