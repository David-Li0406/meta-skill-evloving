// Server Action with useTransition for mutations outside forms

// actions.ts
"use server";

import { revalidatePath } from "next/cache";

async function incrementLike(postId: string) {
  const post = await db.posts.incrementLikes(postId);
  revalidatePath(`/posts/${postId}`);
  return post.likeCount;
}

// like-button.tsx
("use client");

import { useState, useTransition } from "react";

function LikeButton({ postId, initialCount }: { postId: string; initialCount: number }) {
  const [isPending, startTransition] = useTransition();
  const [count, setCount] = useState(initialCount);

  const handleClick = () => {
    startTransition(async () => {
      const newCount = await incrementLike(postId);
      setCount(newCount);
    });
  };

  return (
    <button onClick={handleClick} disabled={isPending}>
      {isPending ? "..." : `♥ ${count}`}
    </button>
  );
}

// Types for example
declare const db: { posts: { incrementLikes: (id: string) => Promise<{ likeCount: number }> } };
export { incrementLike, LikeButton };
