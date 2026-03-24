import fs from "node:fs/promises";

const ORG =
  process.env.ORG_NAME ||
  process.env.GITHUB_REPOSITORY_OWNER ||
  process.env.GITHUB_ACTOR;
const OUTPUT_FILE = process.env.OUTPUT_FILE || "profile/readme.md";
const MAX_ITEMS = Number.parseInt(process.env.MAX_ITEMS || "15", 10);
const EXCLUDE_TYPES = new Set(
  (process.env.EXCLUDE_TYPES || "WatchEvent")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean),
);

const TOKEN = process.env.GITHUB_TOKEN || process.env.TOKEN;

if (!ORG) {
  throw new Error("ORG_NAME (or GITHUB_REPOSITORY_OWNER) is required.");
}
if (!TOKEN) {
  throw new Error("GITHUB_TOKEN (or TOKEN) is required.");
}

function apiHeaders() {
  return {
    Authorization: `Bearer ${TOKEN}`,
    Accept: "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "update-org-activity",
  };
}

function repoUrl(repoFullName) {
  return `https://github.com/${repoFullName}`;
}

function yyyyMmDd(isoString) {
  try {
    return new Date(isoString).toISOString().slice(0, 10);
  } catch {
    return "";
  }
}

function escapeMarkdown(text) {
  return String(text).replace(/[\[\]]/g, "\\$&").trim();
}

function eventToLine(event) {
  const date = yyyyMmDd(event.created_at);
  const actor = event.actor?.login ? `@${event.actor.login}` : "someone";
  const repoFullName = event.repo?.name || "";
  const repoLink = repoFullName ? `[${repoFullName}](${repoUrl(repoFullName)})` : "a repo";

  const type = event.type;
  const payload = event.payload || {};

  if (type === "PushEvent") {
    const commitCount = Array.isArray(payload.commits) ? payload.commits.length : 0;
    const head = payload.head;
    const before = payload.before;

    let targetUrl = repoFullName ? `${repoUrl(repoFullName)}/commits` : "";
    if (repoFullName && head && before && head !== before) {
      targetUrl = `${repoUrl(repoFullName)}/compare/${before}...${head}`;
    } else if (repoFullName && head) {
      targetUrl = `${repoUrl(repoFullName)}/commit/${head}`;
    }

    const commitsText =
      commitCount === 1 ? "1 commit" : commitCount > 1 ? `${commitCount} commits` : "commits";
    return `- ${date} — ${actor} pushed ${commitsText} to ${repoLink}${targetUrl ? ` ([diff](${targetUrl}))` : ""}`;
  }

  if (type === "PullRequestEvent" && payload.pull_request) {
    const action = payload.action || "updated";
    const pr = payload.pull_request;
    const prNumber = pr.number ? `#${pr.number}` : "";
    const title = pr.title ? `: ${escapeMarkdown(pr.title)}` : "";
    return `- ${date} — ${actor} ${action} PR [${prNumber}${title}](${pr.html_url}) in ${repoLink}`;
  }

  if (type === "IssuesEvent" && payload.issue) {
    const action = payload.action || "updated";
    const issue = payload.issue;
    const issueNumber = issue.number ? `#${issue.number}` : "";
    const title = issue.title ? `: ${escapeMarkdown(issue.title)}` : "";
    return `- ${date} — ${actor} ${action} issue [${issueNumber}${title}](${issue.html_url}) in ${repoLink}`;
  }

  if (type === "IssueCommentEvent" && payload.comment) {
    const action = payload.action || "commented on";
    const comment = payload.comment;
    const issueUrl = payload.issue?.html_url || payload.pull_request?.html_url || comment.html_url;
    return `- ${date} — ${actor} ${action} [a thread](${issueUrl}) in ${repoLink}`;
  }

  if (type === "ReleaseEvent" && payload.release) {
    const action = payload.action || "published";
    const release = payload.release;
    const tag = release.tag_name ? ` ${escapeMarkdown(release.tag_name)}` : "";
    return `- ${date} — ${actor} ${action} a release${tag} in ${repoLink} ([link](${release.html_url}))`;
  }

  if (type === "ForkEvent" && payload.forkee?.html_url) {
    return `- ${date} — ${actor} forked ${repoLink} to [${escapeMarkdown(payload.forkee.full_name || "a fork")}](${payload.forkee.html_url})`;
  }

  if (type === "PublicEvent") {
    return `- ${date} — ${actor} made ${repoLink} public`;
  }

  // Fallback: keep it short and still link to the repo.
  return `- ${date} — ${actor} ${escapeMarkdown(type)} in ${repoLink}`;
}

async function fetchJson(url) {
  const res = await fetch(url, { headers: apiHeaders() });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`GitHub API ${res.status} for ${url}${body ? `: ${body}` : ""}`);
  }
  return res.json();
}

async function fetchOrgEvents() {
  const perPage = 100;
  const pages = [1, 2]; // enough to fill MAX_ITEMS after filtering
  const all = [];

  for (const page of pages) {
    const url = `https://api.github.com/orgs/${encodeURIComponent(ORG)}/events?per_page=${perPage}&page=${page}`;
    const events = await fetchJson(url);
    if (!Array.isArray(events) || events.length === 0) break;
    all.push(...events);
    if (all.length >= perPage) break;
  }
  return all;
}

function updateReadme(original, activityLines) {
  const start = "<!-- ORG_ACTIVITY:START -->";
  const end = "<!-- ORG_ACTIVITY:END -->";
  const updatedTag = "<!-- ORG_ACTIVITY_UPDATED -->";
  const updatedAt = new Date().toISOString();
  const updateTimestamp = (text) => {
    if (text.includes(updatedTag)) return text.replace(updatedTag, updatedAt);
    return text.replace(
      /(_Last updated:\s*)(\d{4}-\d{2}-\d{2}T[0-9:.]+Z)(\s*_)/,
      `$1${updatedAt}$3`,
    );
  };

  if (!original.includes(start) || !original.includes(end)) {
    const section = [
      "## Org activity",
      "",
      start,
      ...activityLines,
      end,
      "",
      `_Last updated: ${updatedTag}_`,
      "",
    ].join("\n");
    return updateTimestamp(`${original.trimEnd()}\n\n${section}`);
  }

  const before = original.slice(0, original.indexOf(start) + start.length);
  const after = original.slice(original.indexOf(end));
  const next = `${before}\n${activityLines.join("\n")}\n${after}`;
  return updateTimestamp(next);
}

const allEvents = await fetchOrgEvents();
const lines = [];
for (const ev of allEvents) {
  if (EXCLUDE_TYPES.has(ev.type)) continue;
  const line = eventToLine(ev);
  if (!line) continue;
  lines.push(line);
  if (lines.length >= MAX_ITEMS) break;
}

if (lines.length === 0) {
  lines.push("- _No recent public activity found._");
}

const current = await fs.readFile(OUTPUT_FILE, "utf8");
const next = updateReadme(current, lines);

if (next !== current) {
  await fs.writeFile(OUTPUT_FILE, next, "utf8");
}
