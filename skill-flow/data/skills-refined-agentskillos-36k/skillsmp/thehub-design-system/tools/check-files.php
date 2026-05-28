<?php
/**
 * Check which files exist on the server
 */
require_once __DIR__ . '/../config.php';
require_admin();

error_reporting(E_ALL);
ini_set('display_errors', 0); // Don't display errors in production

echo"<h1>File Existence Check</h1>";
echo"<p>Checking which files are present on the server...</p>";

$filesToCheck = [
 '/admin/series.php' => 'Series management page',
 '/admin/point-templates.php' => 'Point templates page (NEW)',
 '/admin/series-events.php' => 'Series events management page (NEW)',
 '/admin/migrations/add_series_format.php' => 'Format column migration (NEW)',
 '/admin/migrations/create_series_events_and_point_templates.php' => 'Series-events migration (NEW)',
 '/admin/debug-series.php' => 'Debug script (NEW)',
 '/components/sidebar.php' => 'Navigation sidebar (PRIMARY)',
 '/includes/config/admin-tabs-config.php' => 'Admin tabs configuration',
];

echo"<table border='1' cellpadding='10'>";
echo"<tr><th>File</th><th>Status</th><th>Description</th></tr>";

foreach ($filesToCheck as $file => $description) {
 $fullPath = __DIR__ . '/..' . $file;
 $exists = file_exists($fullPath);
 $status = $exists ? '✅ EXISTS' : '❌ MISSING';
 $statusColor = $exists ? 'green' : 'red';

 echo"<tr>";
 echo"<td><code>" . htmlspecialchars($file) ."</code></td>";
 $statusClass = $exists ? 'text-success' : 'text-error';
 echo"<td class='{$statusClass} gs-font-weight-600'>{$status}</td>";
 echo"<td>" . htmlspecialchars($description) ."</td>";
 echo"</tr>";
}

echo"</table>";

echo"<h2>Git Information (if available)</h2>";
if (function_exists('shell_exec')) {
 $gitBranch = @shell_exec('cd ' . __DIR__ . '/.. && git branch 2>&1');
 if ($gitBranch) {
 echo"<pre>" . htmlspecialchars($gitBranch) ."</pre>";
 } else {
 echo"<p>Git not available or not a git repository on live server</p>";
 }
} else {
 echo"<p>shell_exec() is disabled on this server</p>";
}

echo"<h2>Instructions</h2>";
echo"<p>If files are MISSING, you need to deploy them from your development branch to the live server.</p>";
echo"<p>Common deployment methods:</p>";
echo"<ul>";
echo"<li>FTP/SFTP upload</li>";
echo"<li>Git pull (if git is set up on live server)</li>";
echo"<li>File manager in hosting control panel</li>";
echo"</ul>";
?>
