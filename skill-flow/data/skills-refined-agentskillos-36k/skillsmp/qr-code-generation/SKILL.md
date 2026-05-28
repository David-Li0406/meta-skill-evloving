---
name: QR Code Generation
description: Generate and scan QR codes for sharing and verification
---

# QR Code Generation Skill

## Libraries

### qrcode (Node.js/React)
```bash
npm install qrcode react-qr-code
```

### Generate QR Code
```jsx
import QRCode from 'react-qr-code';

export function ShareQRCode({ url }) {
  return (
    <div style={{ background: 'white', padding: 16 }}>
      <QRCode
        value={url}
        size={256}
        level="H"
        fgColor="#000000"
        bgColor="#ffffff"
      />
    </div>
  );
}
```

### Generate to File (Server-side)
```javascript
import QRCode from 'qrcode';

// To file
await QRCode.toFile('qr.png', 'https://smarter.poker/invite/ABC123');

// To data URL
const dataUrl = await QRCode.toDataURL('https://smarter.poker/invite/ABC123');

// To buffer
const buffer = await QRCode.toBuffer('https://smarter.poker/invite/ABC123');
```

### With Logo/Branding
```jsx
import { QRCodeCanvas } from 'qrcode.react';

export function BrandedQRCode({ url }) {
  return (
    <QRCodeCanvas
      value={url}
      size={256}
      level="H"
      includeMargin={true}
      imageSettings={{
        src: '/logo.png',
        x: undefined,
        y: undefined,
        height: 40,
        width: 40,
        excavate: true,
      }}
    />
  );
}
```

## Use Cases

### Invite/Referral Links
```jsx
function ReferralQR({ userId }) {
  const referralUrl = `https://smarter.poker/join?ref=${userId}`;
  
  return (
    <div className="text-center">
      <h3>Invite Friends</h3>
      <QRCode value={referralUrl} size={200} />
      <p>Scan to join with your referral</p>
    </div>
  );
}
```

### Club Invite
```jsx
function ClubInviteQR({ clubId, inviteCode }) {
  const inviteUrl = `https://smarter.poker/club/${clubId}/join?code=${inviteCode}`;
  
  return <QRCode value={inviteUrl} size={180} />;
}
```

### Tournament Entry
```jsx
function TournamentEntryQR({ tournamentId, ticketId }) {
  const entryData = JSON.stringify({
    type: 'tournament_entry',
    tournament: tournamentId,
    ticket: ticketId,
    timestamp: Date.now()
  });
  
  return <QRCode value={entryData} size={200} />;
}
```

## QR Scanning

### html5-qrcode
```bash
npm install html5-qrcode
```

```jsx
import { Html5QrcodeScanner } from 'html5-qrcode';
import { useEffect } from 'react';

export function QRScanner({ onScan }) {
  useEffect(() => {
    const scanner = new Html5QrcodeScanner('qr-reader', {
      fps: 10,
      qrbox: 250
    });
    
    scanner.render(
      (decodedText) => {
        onScan(decodedText);
        scanner.clear();
      },
      (error) => console.warn(error)
    );
    
    return () => scanner.clear();
  }, [onScan]);
  
  return <div id="qr-reader" />;
}
```

## Download/Save QR
```jsx
function DownloadableQR({ url, filename }) {
  const downloadQR = () => {
    const canvas = document.querySelector('canvas');
    const link = document.createElement('a');
    link.download = `${filename}.png`;
    link.href = canvas.toDataURL();
    link.click();
  };
  
  return (
    <>
      <QRCodeCanvas value={url} size={300} />
      <button onClick={downloadQR}>Download QR Code</button>
    </>
  );
}
```
