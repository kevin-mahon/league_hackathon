export function parseAttrName(attrName: string): string {
    // Convert camelCase to Title Case
  return attrName
    .replace(/([A-Z])/g, ' $1')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

export function parseBoolean(value: boolean): string {
    return value ? "Yes" : "No";
}

