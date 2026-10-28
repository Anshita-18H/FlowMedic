export type NormalizedIssue = {
  externalId: string;
  number: number;
  title: string;
  body: string;
  state: "open" | "closed";
  htmlUrl: string;
  updatedAt: string;
};

type GitHubIssue = {
  id: number;
  number: number;
  title: string;
  body: string | null;
  state: string;
  html_url: string;
  updated_at: string;
  pull_request?: unknown;
};

export class GitHubRequestError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly retryAfterSeconds?: number,
  ) {
    super(message);
    this.name = "GitHubRequestError";
  }
}

const pageSize = 50;
const maxPages = 2;
const maxBodyLength = 4000;

export async function fetchRepositoryIssues(owner: string, repository: string, token: string) {
  const issues: NormalizedIssue[] = [];

  for (let page = 1; page <= maxPages; page += 1) {
    const endpoint = new URL(
      `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(repository)}/issues`,
    );
    endpoint.searchParams.set("state", "all");
    endpoint.searchParams.set("per_page", String(pageSize));
    endpoint.searchParams.set("page", String(page));

    const response = await fetch(endpoint, {
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${token}`,
        "X-GitHub-Api-Version": "2022-11-28",
      },
      signal: AbortSignal.timeout(8_000),
      cache: "no-store",
    });

    if (!response.ok) {
      const retryAfter = Number(response.headers.get("retry-after"));
      const rateLimitReset = Number(response.headers.get("x-ratelimit-reset"));
      const waitSeconds = Number.isFinite(retryAfter) && retryAfter > 0
        ? retryAfter
        : Number.isFinite(rateLimitReset) && rateLimitReset > 0
          ? Math.max(1, rateLimitReset - Math.floor(Date.now() / 1000))
          : undefined;
      const rateLimited = response.status === 429 || response.headers.get("x-ratelimit-remaining") === "0";
      const message = rateLimited
        ? `GitHub rate limit reached.${waitSeconds ? ` Retry in about ${waitSeconds} seconds.` : " Retry later."}`
        : response.status === 401 || response.status === 403
        ? "GitHub denied access. Check the token and its repository Issues read permission."
        : response.status === 404
          ? "The configured GitHub repository was not found or is not accessible to this token."
          : `GitHub request failed with status ${response.status}.`;
      throw new GitHubRequestError(message, response.status, waitSeconds);
    }

    const payload = (await response.json()) as GitHubIssue[];
    for (const issue of payload) {
      if (issue.pull_request || !Number.isSafeInteger(issue.id) || !Number.isSafeInteger(issue.number)) {
        continue;
      }

      issues.push({
        externalId: String(issue.id),
        number: issue.number,
        title: issue.title.slice(0, 500),
        body: (issue.body ?? "").slice(0, maxBodyLength),
        state: issue.state === "closed" ? "closed" : "open",
        htmlUrl: issue.html_url,
        updatedAt: issue.updated_at,
      });
    }

    if (payload.length < pageSize) break;
  }

  return issues;
}
