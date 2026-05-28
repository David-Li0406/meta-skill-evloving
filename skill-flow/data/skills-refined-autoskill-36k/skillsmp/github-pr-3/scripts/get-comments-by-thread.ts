#!/usr/bin/env bun
/**
 * スレッドIDからコメント一覧を取得
 */

import { defineCommand, runMain } from "citty";
import { Octokit } from "octokit";

type Comment = {
	id: string;
	databaseId: number;
	author: string;
	body: string;
	url: string;
};

type ThreadCommentsResult = {
	threadId: string;
	path: string;
	line: number | null;
	comments: Comment[];
};

const QUERY = `
  query($threadId: ID!) {
    node(id: $threadId) {
      ... on PullRequestReviewThread {
        id
        path
        line
        comments(first: 100) {
          nodes {
            id
            databaseId
            author { login }
            body
            url
          }
        }
      }
    }
  }
`;

async function fetchThreadComments(
	threadId: string,
): Promise<ThreadCommentsResult> {
	const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

	const result = await octokit.graphql<{
		node: {
			id: string;
			path: string;
			line: number | null;
			comments: {
				nodes: Array<{
					id: string;
					databaseId: number;
					author: { login: string };
					body: string;
					url: string;
				}>;
			};
		};
	}>(QUERY, { threadId });

	return {
		threadId: result.node.id,
		path: result.node.path,
		line: result.node.line,
		comments: result.node.comments.nodes.map((c) => ({
			id: c.id,
			databaseId: c.databaseId,
			author: c.author.login,
			body: c.body,
			url: c.url,
		})),
	};
}

const main = defineCommand({
	meta: {
		name: "get-comments-by-thread",
		description: "スレッドIDからコメント詳細を取得",
	},
	args: {
		threadId: {
			type: "positional",
			description: "スレッドID（PRRT_xxx形式）",
			required: true,
		},
	},
	async run({ args }) {
		const result = await fetchThreadComments(args.threadId);
		console.log(JSON.stringify(result, null, 2));
	},
});

runMain(main);
