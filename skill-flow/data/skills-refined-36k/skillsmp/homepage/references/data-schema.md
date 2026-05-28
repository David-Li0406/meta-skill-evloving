# Homepage Data Schemas

TypeScript interfaces and data files for homepage sections.

All data files are located in `src/content/homepage/`.

## Hero (hero.ts)

```typescript
export interface HeroData {
  name: string;
  title: string;
  overview: string;
  primarySkills: string[];
}

export const hero: HeroData = {
  name: "Muhammad Ramdan",
  title: "Software Engineer",
  overview: "...",
  primarySkills: ["TypeScript", "React", "Node.js", "Python", "Swift"],
};
```

---

## Experience (experience.ts)

```typescript
export interface Role {
  title: string;
  type: string; // "Full-time" | "Part-time" | "Freelance" | "Internship" | "Apprenticeship" | "Self-Employed"
  period: string; // "Mon YYYY - Mon YYYY" or "Mon YYYY - Present"
  bullets: string[];
}

export interface Job {
  company: string;
  location: string; // "City, Country (Remote)" or "City, Country"
  roles: Role[];
}

export const jobs: Job[] = [
  {
    company: "Stockifi",
    location: "Oslo, Norway (Remote)",
    roles: [
      {
        title: "Software Engineer Team Lead",
        type: "Full-time",
        period: "Sep 2024 - Present",
        bullets: ["..."],
      },
    ],
  },
];
```

### Notes

- A company can have multiple roles (career progression)
- Roles within a company are listed in reverse chronological order
- Jobs array is ordered with most recent company first

---

## Education (education.ts)

```typescript
export interface Education {
  institution: string;
  degree: string;
  gpa?: string;
  location: string;
  period: string; // "YYYY - YYYY"
}

export const education: Education[] = [
  {
    institution: "Universitas Pendidikan Indonesia",
    degree: "Electrical Engineering",
    gpa: "3.57/4.00",
    location: "Bandung, Indonesia",
    period: "2019 - 2024",
  },
];
```

---

## Skills (skills.ts)

```typescript
export interface SkillCategory {
  title: string;
  skills: string[];
}

export const skillCategories: SkillCategory[] = [
  {
    title: "Languages",
    skills: [
      "English (Fluent)",
      "Bahasa Indonesia (Native)",
      "Norwegian (Novice)",
    ],
  },
  {
    title: "Web",
    skills: [
      "HTML",
      "CSS",
      "JavaScript",
      "React",
      "Redux",
      "Next.js",
      "TypeScript",
    ],
  },
];
```

### Current Categories

| Category    | Description                                    |
| ----------- | ---------------------------------------------- |
| Languages   | Human languages with proficiency level         |
| Soft Skills | Non-technical professional skills              |
| Web         | Frontend/web technologies                      |
| Mobile      | Mobile development technologies                |
| Additional  | Backend, cloud, ML, and other technical skills |
