#!/usr/bin/env bun
/**
 * 現在のブランチに紐づくPRのスレッドに返信
 */

import { defineCommand, runMain } from "citty";
import { Octokit } from "octokit";
import type { RemoteWithRefs } from "simple-git";
import { simpleGit } from "simple-git";

async function getCurrentPRInfo(): Promise<{
	owner: string;
	repo: string;
	pr: number;
}> {
	const git = simpleGit();

	const remotes = await git.getRemotes(true);
	const origin = remotes.find((r: RemoteWithRefs) => r.name === "origin");
	if (!origin?.refs.fetch) {
		throw new Error("No origin remote found");
	}

	const match = origin.refs.fetch.match(/github\.com[:/]([^/]+)\/([^/.]+)/);
	if (!match) {
		throw new Error("Could not parse GitHub URL from origin");
	}

	const matchedOwner = match[1];
	const matchedRepo = match[2];
	if (!matchedOwner || !matchedRepo) {
		throw new Error("Could not extract owner/repo from origin");
	}

	const branch = await git.revparse(["--abbrev-ref", "HEAD"]);

	const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
	const repoName = matchedRepo.replace(/\.git$/, "");

	const { data: prs } = await octokit.rest.pulls.list({
		owner: matchedOwner,
		repo: repoName,
		head: `${matchedOwner}:${branch.trim()}`,
		state: "open",
	});

	const firstPr = prs[0];
	if (!firstPr) {
		throw new Error(`No open PR found for branch: ${branch.trim()}`);
	}

	return {
		owner: matchedOwner,
		repo: repoName,
		pr: firstPr.number,
	};
}

async function resolveCommentId(
	input: string,
	owner: string,
	repo: string,
	pr: number,
): Promise<number> {
	if (/^\d+$/.test(input)) {
		return Number.parseInt(input, 10);
	}

	const urlMatch = input.match(/discussion_r(\d+)/);
	if (urlMatch?.[1]) {
		return Number.parseInt(urlMatch[1], 10);
	}

	if (input.startsWith("PRRC_")) {
		const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

		const result = await octokit.graphql<{
			repository: {
				pullRequest: {
					reviewThreads: {
						nodes: Array<{
							comments: {
								nodes: Array<{ id: string; databaseId: number }>;
							};
						}>;
					};
				};
			};
		}>(
			`query($owner: String!, $repo: String!, $pr: Int!) {
        repository(owner: $owner, name: $repo) {
          pullRequest(number: $pr) {
            reviewThreads(first: 100) {
              nodes {
                comments(first: 100) {
                  nodes { id databaseId }
                }
              }
            }
          }
        }
      }`,
			{ owner, repo, pr },
		);

		const found = result.repository.pullRequest.reviewThreads.nodes
			.flatMap((thread) => thread.comments.nodes)
			.find((comment) => comment.id === input);

		if (!found) {
			throw new Error(`Could not find comment with GraphQL ID: ${input}`);
		}

		return found.databaseId;
	}

	throw new Error(`Cannot resolve comment ID from: ${input}`);
}

async function replyToComment(
	owner: string,
	repo: string,
	pr: number,
	commentId: number,
	body: string,
): Promise<void> {
	const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

	const response = await octokit.rest.pulls.createReplyForReviewComment({
		owner,
		repo,
		pull_number: pr,
		comment_id: commentId,
		body,
	});

	console.log(JSON.stringify(response.data, null, 2));
}

const main = defineCommand({
	meta: {
		name: "reply-to-thread",
		description: "スレッドに返信",
	},
	args: {
		commentId: {
			type: "positional",
			description: "コメントID（databaseId数値 / URL / GraphQL ID PRRC_xxx）",
			required: true,
		},
		body: {
			type: "positional",
			description: "返信内容",
			required: true,
		},
	},
	async run({ args }) {
		const { owner, repo, pr } = await getCurrentPRInfo();
		const resolvedId = await resolveCommentId(args.commentId, owner, repo, pr);
		await replyToComment(owner, repo, pr, resolvedId, args.body);
	},
});

runMain(main);
