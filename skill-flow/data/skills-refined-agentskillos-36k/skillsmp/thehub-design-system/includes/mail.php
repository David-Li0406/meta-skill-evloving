<?php
/**
 * TheHUB Email Helper
 * Supports Resend (recommended), SMTP, and PHP mail()
 * Configure in .env file - set MAIL_DRIVER=resend for best deliverability
 */

/**
 * Send an email using configured driver
 *
 * @param string $to Recipient email address
 * @param string $subject Email subject
 * @param string $body Email body (HTML supported)
 * @param array $options Optional settings (from_name, from_email, reply_to)
 * @return bool True if mail was accepted for delivery
 */
function hub_send_email(string $to, string $subject, string $body, array $options = []): bool {
    // Get mail configuration from environment
    $mailDriver = env('MAIL_DRIVER', 'mail'); // 'resend', 'smtp', or 'mail'

    // Default sender info (from .env or fallback)
    $fromName = $options['from_name'] ?? env('MAIL_FROM_NAME', 'TheHUB');
    $fromEmail = $options['from_email'] ?? env('MAIL_FROM_ADDRESS', 'info@gravityseries.se');
    $replyTo = $options['reply_to'] ?? $fromEmail;

    // Log the email attempt
    error_log("TheHUB Mail: Sending to {$to} - Subject: {$subject} - Driver: {$mailDriver}");

    if ($mailDriver === 'resend') {
        return hub_send_resend_email($to, $subject, $body, $fromName, $fromEmail, $replyTo);
    } elseif ($mailDriver === 'smtp') {
        return hub_send_smtp_email($to, $subject, $body, $fromName, $fromEmail, $replyTo);
    } else {
        return hub_send_php_mail($to, $subject, $body, $fromName, $fromEmail, $replyTo);
    }
}

/**
 * Send email using Resend API (recommended for best deliverability)
 */
function hub_send_resend_email(string $to, string $subject, string $body, string $fromName, string $fromEmail, string $replyTo): bool {
    $apiKey = env('RESEND_API_KEY', '');

    if (empty($apiKey)) {
        error_log("TheHUB Mail: Resend API key not configured, falling back to SMTP");
        return hub_send_smtp_email($to, $subject, $body, $fromName, $fromEmail, $replyTo);
    }

    $data = [
        'from' => "{$fromName} <{$fromEmail}>",
        'to' => [$to],
        'subject' => $subject,
        'html' => $body,
        'reply_to' => $replyTo
    ];

    $ch = curl_init('https://api.resend.com/emails');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer ' . $apiKey,
            'Content-Type: application/json'
        ],
        CURLOPT_POSTFIELDS => json_encode($data),
        CURLOPT_TIMEOUT => 30
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    if ($error) {
        error_log("TheHUB Mail: Resend cURL error: {$error}");
        return false;
    }

    $result = json_decode($response, true);

    if ($httpCode >= 200 && $httpCode < 300 && isset($result['id'])) {
        error_log("TheHUB Mail: Email sent successfully via Resend to {$to} (ID: {$result['id']})");
        return true;
    } else {
        $errorMsg = $result['message'] ?? $result['error'] ?? $response;
        error_log("TheHUB Mail: Resend error (HTTP {$httpCode}): {$errorMsg}");
        return false;
    }
}

/**
 * Send email using PHP's native mail() function
 */
function hub_send_php_mail(string $to, string $subject, string $body, string $fromName, string $fromEmail, string $replyTo): bool {
    $headers = [];
    $headers[] = 'MIME-Version: 1.0';
    $headers[] = 'Content-Type: text/html; charset=UTF-8';
    $headers[] = "From: {$fromName} <{$fromEmail}>";
    $headers[] = "Reply-To: {$fromEmail}"; // Use from email as reply-to
    $headers[] = 'X-Mailer: TheHUB/1.0';

    $result = @mail($to, $subject, $body, implode("\r\n", $headers));

    if (!$result) {
        error_log("TheHUB Mail: PHP mail() failed to send to {$to}");
    }

    return $result;
}

/**
 * Send email using SMTP
 */
function hub_send_smtp_email(string $to, string $subject, string $body, string $fromName, string $fromEmail, string $replyTo): bool {
    $host = env('MAIL_HOST', 'smtp.hostinger.com'); // smtp.hostinger.com works, mail.hostinger.com doesn't
    $port = (int) env('MAIL_PORT', 465);
    $encryption = env('MAIL_ENCRYPTION', 'ssl');
    $username = env('MAIL_USERNAME', '');
    $password = env('MAIL_PASSWORD', '');

    // Debug logging
    error_log("TheHUB Mail SMTP: Connecting to {$host}:{$port} ({$encryption}) as {$username}");

    if (empty($username) || empty($password)) {
        error_log("TheHUB Mail: SMTP credentials not configured - username: " . ($username ?: 'empty') . ", password: " . ($password ? 'set' : 'empty'));
        // Fallback to PHP mail
        return hub_send_php_mail($to, $subject, $body, $fromName, $fromEmail, $replyTo);
    }

    try {
        // Connect to SMTP server
        $context = stream_context_create([
            'ssl' => [
                'verify_peer' => false,
                'verify_peer_name' => false,
                'allow_self_signed' => true
            ]
        ]);

        $protocol = ($encryption === 'ssl') ? 'ssl://' : '';
        $socket = @stream_socket_client(
            "{$protocol}{$host}:{$port}",
            $errno,
            $errstr,
            10,
            STREAM_CLIENT_CONNECT,
            $context
        );

        if (!$socket) {
            error_log("TheHUB Mail: SMTP connection failed: {$errstr} ({$errno})");
            return false;
        }

        // Read greeting
        $response = fgets($socket, 515);
        if (substr($response, 0, 3) !== '220') {
            error_log("TheHUB Mail: SMTP greeting failed: {$response}");
            fclose($socket);
            return false;
        }

        // EHLO
        fputs($socket, "EHLO " . gethostname() . "\r\n");
        $response = hub_smtp_get_response($socket);

        // Start TLS if using TLS encryption (port 587)
        if ($encryption === 'tls' && strpos($response, 'STARTTLS') !== false) {
            fputs($socket, "STARTTLS\r\n");
            $response = fgets($socket, 515);
            if (substr($response, 0, 3) !== '220') {
                error_log("TheHUB Mail: STARTTLS failed: {$response}");
                fclose($socket);
                return false;
            }
            stream_socket_enable_crypto($socket, true, STREAM_CRYPTO_METHOD_TLS_CLIENT);
            fputs($socket, "EHLO " . gethostname() . "\r\n");
            hub_smtp_get_response($socket);
        }

        // AUTH LOGIN
        fputs($socket, "AUTH LOGIN\r\n");
        $response = fgets($socket, 515);
        if (substr($response, 0, 3) !== '334') {
            error_log("TheHUB Mail: AUTH LOGIN failed: {$response}");
            fclose($socket);
            return false;
        }

        // Send username
        fputs($socket, base64_encode($username) . "\r\n");
        $response = fgets($socket, 515);
        if (substr($response, 0, 3) !== '334') {
            error_log("TheHUB Mail: Username rejected: {$response}");
            fclose($socket);
            return false;
        }

        // Send password
        fputs($socket, base64_encode($password) . "\r\n");
        $response = fgets($socket, 515);
        if (substr($response, 0, 3) !== '235') {
            error_log("TheHUB Mail: Authentication failed: {$response}");
            fclose($socket);
            return false;
        }

        // MAIL FROM
        fputs($socket, "MAIL FROM:<{$fromEmail}>\r\n");
        $response = fgets($socket, 515);
        if (substr($response, 0, 3) !== '250') {
            error_log("TheHUB Mail: MAIL FROM rejected: {$response}");
            fclose($socket);
            return false;
        }

        // RCPT TO
        fputs($socket, "RCPT TO:<{$to}>\r\n");
        $response = fgets($socket, 515);
        if (substr($response, 0, 3) !== '250' && substr($response, 0, 3) !== '251') {
            error_log("TheHUB Mail: RCPT TO rejected: {$response}");
            fclose($socket);
            return false;
        }

        // DATA
        fputs($socket, "DATA\r\n");
        $response = fgets($socket, 515);
        if (substr($response, 0, 3) !== '354') {
            error_log("TheHUB Mail: DATA rejected: {$response}");
            fclose($socket);
            return false;
        }

        // Build email headers and body
        $headers = "From: {$fromName} <{$fromEmail}>\r\n";
        $headers .= "Reply-To: {$replyTo}\r\n";
        $headers .= "To: {$to}\r\n";
        $headers .= "Subject: {$subject}\r\n";
        $headers .= "MIME-Version: 1.0\r\n";
        $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
        $headers .= "X-Mailer: TheHUB/1.0\r\n";
        $headers .= "\r\n";

        // Send headers and body (escape dots at start of lines)
        $body = str_replace("\n.", "\n..", $body);
        fputs($socket, $headers . $body . "\r\n.\r\n");

        $response = fgets($socket, 515);
        if (substr($response, 0, 3) !== '250') {
            error_log("TheHUB Mail: Message rejected: {$response}");
            fclose($socket);
            return false;
        }

        // QUIT
        fputs($socket, "QUIT\r\n");
        fclose($socket);

        error_log("TheHUB Mail: Email sent successfully via SMTP to {$to}");
        return true;

    } catch (Exception $e) {
        error_log("TheHUB Mail: SMTP error: " . $e->getMessage());
        return false;
    }
}

/**
 * Read multi-line SMTP response
 */
function hub_smtp_get_response($socket): string {
    $response = '';
    while ($line = fgets($socket, 515)) {
        $response .= $line;
        // If 4th character is a space, this is the last line
        if (isset($line[3]) && $line[3] === ' ') {
            break;
        }
    }
    return $response;
}

/**
 * Send password reset email
 */
function hub_send_password_reset_email(string $email, string $name, string $resetLink): bool {
    $subject = 'Återställ ditt lösenord - TheHUB';

    $body = hub_email_template('password_reset', [
        'name' => $name,
        'reset_link' => $resetLink,
        'expires' => '24 timmar'
    ]);

    return hub_send_email($email, $subject, $body);
}

/**
 * Send account activation email
 */
function hub_send_account_activation_email(string $email, string $name, string $activationLink): bool {
    $subject = 'Aktivera ditt konto - TheHUB';

    $body = hub_email_template('account_activation', [
        'name' => $name,
        'activation_link' => $activationLink,
        'expires' => '24 timmar'
    ]);

    return hub_send_email($email, $subject, $body);
}

/**
 * Get email template with variables replaced
 */
function hub_email_template(string $template, array $vars = []): string {
    // Base styles for email
    $styles = '
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .card { background: #ffffff; border-radius: 12px; padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 24px; }
        .logo { font-size: 24px; font-weight: bold; color: #61CE70; }
        h1 { font-size: 24px; margin: 0 0 16px 0; color: #111; }
        p { margin: 0 0 16px 0; }
        .text-center { text-align: center; }
        .btn { display: inline-block; background: #61CE70; color: #111 !important; padding: 14px 28px; border-radius: 8px; text-decoration: none; font-weight: 600; margin: 16px 0; }
        .link { word-break: break-all; color: #666; font-size: 14px; background: #f5f5f5; padding: 12px; border-radius: 6px; margin: 16px 0; }
        .footer { text-align: center; margin-top: 24px; padding-top: 24px; border-top: 1px solid #eee; color: #666; font-size: 14px; }
        .note { font-size: 14px; color: #666; }
    ';

    // Templates
    $templates = [
        'password_reset' => '
            <div class="header">
                <div class="logo">TheHUB</div>
            </div>
            <h1>Återställ ditt lösenord</h1>
            <p>Hej {{name}},</p>
            <p>Vi har fått en förfrågan om att återställa lösenordet för ditt konto på TheHUB.</p>
            <p>Klicka på knappen nedan för att välja ett nytt lösenord:</p>
            <p class="text-center">
                <a href="{{reset_link}}" class="btn">Återställ lösenord</a>
            </p>
            <p class="note">Eller kopiera och klistra in denna länk i din webbläsare:</p>
            <div class="link">{{reset_link}}</div>
            <p class="note">Länken är giltig i {{expires}}. Om du inte begärde denna återställning kan du ignorera detta mail.</p>
        ',

        'welcome' => '
            <div class="header">
                <div class="logo">TheHUB</div>
            </div>
            <h1>Välkommen till TheHUB!</h1>
            <p>Hej {{name}},</p>
            <p>Ditt konto har skapats på TheHUB - plattformen för gravity racing i Sverige.</p>
            <p>Du kan nu logga in och se dina resultat, anmäla dig till tävlingar och mer.</p>
            <p class="text-center">
                <a href="{{login_link}}" class="btn">Logga in</a>
            </p>
        ',

        'account_activation' => '
            <div class="header">
                <div class="logo">TheHUB</div>
            </div>
            <h1>Aktivera ditt konto</h1>
            <p>Hej {{name}},</p>
            <p>Vi har hittat ditt konto i TheHUB - plattformen för gravity racing i Sverige.</p>
            <p>För att aktivera ditt konto och skapa ett lösenord, klicka på knappen nedan:</p>
            <p class="text-center">
                <a href="{{activation_link}}" class="btn">Aktivera konto</a>
            </p>
            <p class="note">Eller kopiera och klistra in denna länk i din webbläsare:</p>
            <div class="link">{{activation_link}}</div>
            <p class="note">Länken är giltig i {{expires}}. Om du inte begärde denna aktivering kan du ignorera detta mail.</p>
        ',

        'claim_approved' => '
            <div class="header">
                <div class="logo">TheHUB</div>
            </div>
            <h1>Din profil är aktiverad!</h1>
            <p>Hej {{name}},</p>
            <p>Din begäran om att aktivera din profil på TheHUB har godkänts.</p>
            <p>Klicka på knappen nedan för att sätta ditt lösenord och logga in:</p>
            <p class="text-center">
                <a href="{{activation_link}}" class="btn">Aktivera konto</a>
            </p>
            <p class="note">Länken är giltig i {{expires}}.</p>
        ',

        'winback_invitation' => '
            <div class="header">
                <div class="logo">TheHUB</div>
            </div>
            <h1>Vi saknar dig!</h1>
            <p>Hej {{name}},</p>
            <p>Vi har märkt att du inte tävlat på ett tag och vill gärna höra hur du mår och vad vi kan göra bättre.</p>
            <p>Svara på en kort enkät (tar bara 2 minuter) så får du en <strong>{{discount_text}}</strong> på din nästa anmälan som tack!</p>
            <p class="text-center">
                <a href="{{survey_link}}" class="btn">Svara på enkäten</a>
            </p>
            <p class="note">Din feedback är anonym och hjälper oss att skapa bättre tävlingar.</p>
            <p class="note">Eller kopiera och klistra in denna länk i din webbläsare:</p>
            <div class="link">{{survey_link}}</div>
        '
    ];

    // Get template content
    $content = $templates[$template] ?? '<p>Email template not found.</p>';

    // Replace variables
    foreach ($vars as $key => $value) {
        $content = str_replace('{{' . $key . '}}', htmlspecialchars($value), $content);
    }

    // Wrap in full HTML email structure
    $html = '<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TheHUB</title>
    <style>' . $styles . '</style>
</head>
<body>
    <div class="container">
        <div class="card">
            ' . $content . '
        </div>
        <div class="footer">
            <p>TheHUB - Gravity Racing Sverige</p>
            <p><a href="https://thehub.gravityseries.se">thehub.gravityseries.se</a></p>
        </div>
    </div>
</body>
</html>';

    return $html;
}
