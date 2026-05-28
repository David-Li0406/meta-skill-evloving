import { redirect } from 'next/navigation';

export default function ReferralLandingPage({ params }: { params: { code: string } }) {
    const code = (params.code || '').trim();
    if (!code) redirect('/onboarding');

    redirect(`/onboarding?ref=${encodeURIComponent(code)}`);
}

