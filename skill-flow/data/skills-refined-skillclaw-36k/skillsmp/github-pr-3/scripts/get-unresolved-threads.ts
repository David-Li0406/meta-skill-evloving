#!/usr/bin/env bun
/**
 * 現在のブランチに紐づくPRの未解決スレッドIDを取得
 */

import { defineCommand, runMain } from "citty";
import { Octokit } from "octokit";
import type { RemoteWithRefs } from "simple-git";
import { simpleGit } from "simple-git";

type UnresolvedThreadsResult = {
	owner: string;
	repo: string;
	pr: number;
	threadIds: string[];
};

const QUERY = `
  query($owner: String!, $repo: String!, $pr: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $pr) {
        reviewThreads(first: 100) {
          nodes {
            id
            isResolved
            isOutdated
          }
        }
      }
    }
  }
`;

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

async function fetchUnresolvedThreads(
	owner: string,
	repo: string,
	pr: number,
): Promise<UnresolvedThreadsResult> {
	const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

	const result = await octokit.graphql<{
		repository: {
			pullRequest: {
				reviewThreads: {
					nodes: Array<{
						id: string;
						isResolved: boolean;
						isOutdated: boolean;
					}>;
				};
			};
		};
	}>(QUERY, { owner, repo, pr });

	const threadIds = result.repository.pullRequest.reviewThreads.nodes
		.filter((thread) => !thread.isResolved && !thread.isOutdated)
		.map((thread) => thread.id);

	return { owner, repo, pr, threadIds };
}

const main = defineCommand({
	meta: {
		name: "get-unresolved-threads",
		description: "未解決スレッドID一覧を取得",
	},
	async run() {
		const { owner, repo, pr } = await getCurrentPRInfo();
		const result = await fetchUnresolvedThreads(owner, repo, pr);
		console.log(JSON.stringify(result, null, 2));
	},
});

runMain(main);
