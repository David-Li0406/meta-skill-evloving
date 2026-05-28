---
name: prompt-engineer
description: Expert AI Prompt Engineering for the Virtual Try-On and Stylist features.
---

# AI Prompt Engineer Skill

This skill enables the agent to design, test, and refine high-quality prompts for the Gemini/Edge Function pipeline, ensuring consistent results in virtual try-ons and fashion analysis.

## Core Capabilities
- **Try-On Optimization**: Crafting prompts that respect `viewAngle` (front/back/side) and `fit` (tight/regular/oversized).
- **Stylist Consistency**: Ensuring fashion tips and item descriptions maintain a premium, professional "Vogue-like" tone.
- **Visual Consistency**: Techniques to maintain character/model identity across different generations (seed management, keepPose logic).

## References
- Virtual Try-On Prompt Builder: `supabase/functions/virtual-try-on/index.ts`
- AI Service types: `src/services/aiService.ts`

## Standard Prompt Patterns
- Always specify lighting: "Studio lighting, uniform background".
- For Back views: "Back view capture, showing clothing details from behind".
- For Fit: Use keywords like "skintight", "classic straight cut", or "voluminous oversized silhouette".
