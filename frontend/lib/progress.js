// Persists which milestone objectives a student has ticked off, keyed by goal
// so progress survives refreshes and returns if the same plan is regenerated.

const PREFIX = "cm:progress:";

function storageKey(namespace) {
  // Namespace by goal text so different plans don't collide.
  let hash = 0;
  for (let i = 0; i < namespace.length; i++) {
    hash = (hash * 31 + namespace.charCodeAt(i)) | 0;
  }
  return `${PREFIX}${hash}`;
}

export function loadChecked(namespace) {
  if (typeof window === "undefined" || !namespace) return new Set();
  try {
    const raw = window.localStorage.getItem(storageKey(namespace));
    return raw ? new Set(JSON.parse(raw)) : new Set();
  } catch {
    return new Set();
  }
}

export function saveChecked(namespace, checkedSet) {
  if (typeof window === "undefined" || !namespace) return;
  try {
    window.localStorage.setItem(
      storageKey(namespace),
      JSON.stringify([...checkedSet])
    );
  } catch {
    // storage full or blocked — ignore, progress just won't persist
  }
}

// Stable id for one objective within a plan.
export function objectiveKey(week, index, text) {
  return `${week}::${index}::${text}`;
}
