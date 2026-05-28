export function output(data: any): void {
  console.log(JSON.stringify(data, null, 2));
}

export function fail(message: string): never {
  console.error(`Error: ${message}`);
  process.exit(1);
}
