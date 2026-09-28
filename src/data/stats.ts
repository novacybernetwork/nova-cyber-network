/**
 * Homepage / About statistics.
 *
 * Update `value` as the organization grows — keep these honest and never
 * hard-code numbers that haven't actually happened yet. "—" renders cleanly
 * as "not yet published" until you have a real count to put in its place
 * (a bracketed placeholder like "[MEMBER_COUNT]" is too long to display as
 * a stat and will wrap awkwardly, so avoid that pattern here specifically).
 */

export interface Stat {
  label: string;
  value: string;
}

export const stats: Stat[] = [
  { label: "Members", value: "35" },
  { label: "Schools Represented", value: "3" },
  { label: "CTFs Hosted", value: "0" },
  { label: "Challenges Released", value: "0" },
];

export const statsNote =
  "We're a newly founded community — these numbers will grow as our first events launch. Check back often.";
