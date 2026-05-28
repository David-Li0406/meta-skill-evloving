#!/usr/bin/env bun
/**
 * 現在のブランチに紐づくPRのCI状態を取得
 */

import { defineCommand, runMain } from "citty";
import { Octokit } from "octokit";
import type { RemoteWithRefs } from "simple-git";
import { simpleGit } from "simple-git";

type CheckRun = {
	name: string;
	status: string;
	conclusion: string | null;
	detailsUrl: string | null;
};

type CIStatusResult = {
	owner: string;
	repo: string;
	pr: number;
	headSha: string;
	overallStatus: "success" | "failure" | "pending" | "neutral";
	checks: CheckRun[];
};

async function getCurrentPRInfo(): Promise<{
	owner: string;
	repo: string;
	pr: number;
	headSha: string;
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
		headSha: firstPr.head.sha,
	};
}

async function fetchCIStatus(
	owner: string,
	repo: string,
	headSha: string,
	pr: number,
): Promise<CIStatusResult> {
	const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

	const { data: checkRuns } = await octokit.rest.checks.listForRef({
		owner,
		repo,
		ref: headSha,
	});

	const checks: CheckRun[] = checkRuns.check_runs.map((run) => ({
		name: run.name,
		status: run.status,
		conclusion: run.conclusion,
		detailsUrl: run.details_url,
	}));

	let overallStatus: CIStatusResult["overallStatus"] = "success";

	for (const check of checks) {
		if (check.status !== "completed") {
			overallStatus = "pending";
			break;
		}
		if (check.conclusion === "failure" || check.conclusion === "timed_out") {
			overallStatus = "failure";
			break;
		}
		if (check.conclusion === "neutral" || check.conclusion === "skipped") {
			if (overallStatus === "success") {
				overallStatus = "neutral";
			}
		}
	}

	return { owner, repo, pr, headSha, overallStatus, checks };
}

const main = defineCommand({
	meta: {
		name: "get-ci-status",
		description: "PRのCI状態を取得",
	},
	async run() {
		const { owner, repo, pr, headSha } = await getCurrentPRInfo();
		const result = await fetchCIStatus(owner, repo, headSha, pr);
		console.log(JSON.stringify(result, null, 2));
	},
});

runMain(main);
