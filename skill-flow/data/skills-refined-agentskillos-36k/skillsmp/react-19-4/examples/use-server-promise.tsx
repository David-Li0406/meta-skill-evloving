import { Suspense } from "react";
import { use } from "react";

// Never await in server components - blocks rendering
// Pass promise to client, use Suspense for non-blocking streaming

// page.tsx (server) - pass promise, don't await
function Page() {
  const dataPromise = fetchData();
  return (
    <Suspense fallback={<Skeleton />}>
      <DataDisplay dataPromise={dataPromise} />
    </Suspense>
  );
}

// data-display.tsx (client) - use() suspends until resolved
("use client");

function DataDisplay({ dataPromise }: { dataPromise: Promise<Data> }) {
  const data = use(dataPromise);
  return <div>{data.name}</div>;
}

// Types for example
type Data = { name: string };
declare function fetchData(): Promise<Data>;
declare function Skeleton(): JSX.Element;
