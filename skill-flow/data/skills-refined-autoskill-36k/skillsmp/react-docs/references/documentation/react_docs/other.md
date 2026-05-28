# React_Docs - Other

**Pages:** 4

---

## React Blog

**URL:** https://react.dev/blog

**Contents:**
- React Blog
- Denial of Service and Source Code Exposure in React Server Components
- Critical Security Vulnerability in React Server Components
- React Conf 2025 Recap
- React Compiler v1.0
- Introducing the React Foundation
- React 19.2
- React Labs: View Transitions, Activity, and more
- Sunsetting Create React App
- React v19

This blog is the official source for the updates from the React team. Anything important, including release notes or deprecation notices, will be posted here first.

You can also follow the @react.dev account on Bluesky, or @reactjs account on Twitter, but you won’t miss anything essential if you only read this blog.

Security researchers have found and disclosed two additional vulnerabilities in React Server Components while attempting to exploit the patches in last week’s critical vulnerability…

There is an unauthenticated remote code execution vulnerability in React Server Components. A fix has been published in versions 19.0.1, 19.1.2, and 19.2.1. We recommend upgrading immediately.

Last week we hosted React Conf 2025. In this post, we summarize the talks and announcements from the event…

We’re releasing the compiler’s first stable release today, plus linting and tooling improvements to make adoption easier.

Today, we’re announcing our plans to create the React Foundation and a new technical governance structure …

React 19.2 adds new features like Activity, React Performance Tracks, useEffectEvent, and more. In this post …

In React Labs posts, we write about projects in active research and development. In this post, we’re sharing two new experimental features that are ready to try today, and sharing other areas we’re working on now …

Today, we’re deprecating Create React App for new apps, and encouraging existing apps to migrate to a framework, or to migrate to a build tool like Vite, Parcel, or RSBuild. We’re also providing docs for when a framework isn’t a good fit for your project, you want to build your own framework, or you just want to learn how React works by building a React app from scratch …

In the React 19 Upgrade Guide, we shared step-by-step instructions for upgrading your app to React 19. In this post, we’ll give an overview of the new features in React 19, and how you can adopt them …

We announced an experimental release of React Compiler at React Conf 2024. We’ve made a lot of progress since then, and in this post we want to share what’s next for React Compiler …

Last week we hosted React Conf 2024, a two-day conference in Henderson, Nevada where 700+ attendees gathered in-person to discuss the latest in UI engineering. This was our first in-person conference since 2019, and we were thrilled to be able to bring the community together again …

The improvements added to React 19 require some breaking changes, but we’ve worked to make the upgrade as smooth as possible, and we don’t expect the changes to impact most apps. In this post, we will guide you through the steps for upgrading libraries to React 19 …

In React Labs posts, we write about projects in active research and development. Since our last update, we’ve made significant progress on React Compiler, new features, and React 19, and we’d like to share what we learned.

Traditionally, new React features used to only be available at Meta first, and land in the open source releases later. We’d like to offer the React community an option to adopt individual new features as soon as their design is close to final—similar to how Meta uses React internally. We are introducing a new officially supported Canary release channel. It lets curated setups like frameworks decouple adoption of individual React features from the React release schedule.

In React Labs posts, we write about projects in active research and development. Since our last update, we’ve made significant progress on React Server Components, Asset Loading, Optimizing Compiler, Offscreen Rendering, and Transition Tracing, and we’d like to share what we learned.

Today we are thrilled to launch react.dev, the new home for React and its documentation. In this post, we would like to give you a tour of the new site.

React 18 was years in the making, and with it brought valuable lessons for the React team. Its release was the result of many years of research and exploring many paths. Some of those paths were successful; many more were dead-ends that led to new insights. One lesson we’ve learned is that it’s frustrating for the community to wait for new features without having insight into these paths that we’re exploring…

React 18 is now available on npm! In our last post, we shared step-by-step instructions for upgrading your app to React 18. In this post, we’ll give an overview of what’s new in React 18, and what it means for the future…

As we shared in the release post, React 18 introduces features powered by our new concurrent renderer, with a gradual adoption strategy for existing applications. In this post, we will guide you through the steps for upgrading to React 18…

Last week we hosted our 6th React Conf. In previous years, we’ve used the React Conf stage to deliver industry changing announcements such as React Native and React Hooks. This year, we shared our multi-platform vision for React, starting with the release of React 18 and gradual adoption of concurrent features…

The React team is excited to share a few updates:

2020 has been a long year. As it comes to an end we wanted to share a special Holiday Update on our research into zero-bundle-size React Server Components. To introduce React Server Components, we have prepared a talk and a demo. If you want, you can check them out during the holidays, or later when work picks back up in the new year…

Not every React release deserves its own blog post, but you can find a detailed changelog for every release in the CHANGELOG.md file in the React repository, as well as on the Releases page.

---

## React Community

**URL:** https://react.dev/community

**Contents:**
- React Community
- Code of Conduct
- Stack Overflow
- Popular Discussion Forums
- News

React has a community of millions of developers. On this page we’ve listed some React-related communities that you can be a part of; see the other pages in this section for additional online and in-person learning materials.

Before participating in React’s communities, please read our Code of Conduct. We have adopted the Contributor Covenant and we expect that all community members adhere to the guidelines within.

Stack Overflow is a popular forum to ask code-level questions or if you’re stuck with a specific error. Read through the existing questions tagged with reactjs or ask your own!

There are many online forums which are a great place for discussion about best practices and application architecture as well as the future of React. If you have an answerable code-level question, Stack Overflow is usually a better fit.

Each community consists of many thousands of React users.

For the latest news about React, follow @reactjs on Twitter, @react.dev on Bluesky and the official React blog on this website.

---

## React

**URL:** https://react.dev/

**Contents:**
- React
- Create user interfaces from components
  - Video.js
  - My video
- Write components with code and markup
  - VideoList.js
- 3 Videos
  - First video
  - Second video
  - Third video

The library for web and native user interfaces

React lets you build user interfaces out of individual pieces called components. Create your own React components like Thumbnail, LikeButton, and Video. Then combine them into entire screens, pages, and apps.

Whether you work on your own or with thousands of other developers, using React feels the same. It is designed to let you seamlessly combine components written by independent people, teams, and organizations.

React components are JavaScript functions. Want to show some content conditionally? Use an if statement. Displaying a list? Try array map(). Learning React is learning programming.

This markup syntax is called JSX. It is a JavaScript syntax extension popularized by React. Putting JSX markup close to related rendering logic makes React components easy to create, maintain, and delete.

React components receive data and return what should appear on the screen. You can pass them new data in response to an interaction, like when the user types into an input. React will then update the screen to match the new data.

A brief history of React

The origin story of React

Sophie Alpert and Dan Abramov (2018)

Dan Abramov and Lauren Tan (2020)

You don’t have to build your whole page in React. Add React to your existing HTML page, and render interactive React components anywhere on it.

React is a library. It lets you put components together, but it doesn’t prescribe how to do routing and data fetching. To build an entire app with React, we recommend a full-stack React framework like Next.js or React Router.

Eric Rozell and Steven Moyes

React is also an architecture. Frameworks that implement it let you fetch data in asynchronous components that run on the server or even during the build. Read data from a file or a database, and pass it down to your interactive components.

People love web and native apps for different reasons. React lets you build both web apps and native apps using the same skills. It leans upon each platform’s unique strengths to let your interfaces feel just right on every platform.

People expect web app pages to load fast. On the server, React lets you start streaming HTML while you’re still fetching data, progressively filling in the remaining content before any JavaScript code loads. On the client, React can use standard web APIs to keep your UI responsive even in the middle of rendering.

People expect native apps to look and feel like their platform. React Native and Expo let you build apps in React for Android, iOS, and more. They look and feel native because their UIs are truly native. It’s not a web view—your React components render real Android and iOS views provided by the platform.

With React, you can be a web and a native developer. Your team can ship to many platforms without sacrificing the user experience. Your organization can bridge the platform silos, and form teams that own entire features end-to-end.

React approaches changes with care. Every React commit is tested on business-critical surfaces with over a billion users. Over 100,000 React components at Meta help validate every migration strategy.

The React team is always researching how to improve React. Some research takes years to pay off. React has a high bar for taking a research idea into production. Only proven approaches become a part of React.

You’re not alone. Two million developers from all over the world visit the React docs every month. React is something that people and teams can agree on.

This is why React is more than a library, an architecture, or even an ecosystem. React is a community. It’s a place where you can ask for help, find opportunities, and meet new friends. You will meet both developers and designers, beginners and experts, researchers and artists, teachers and students. Our backgrounds may be very different, but React lets us all create user interfaces together.

**Examples:**

Example 1 (jsx):
```jsx
function Video({ video }) {  return (    <div>      <Thumbnail video={video} />      <a href={video.url}>        <h3>{video.title}</h3>        <p>{video.description}</p>      </a>      <LikeButton video={video} />    </div>  );}
```

Example 2 (javascript):
```javascript
function VideoList({ videos, emptyHeading }) {  const count = videos.length;  let heading = emptyHeading;  if (count > 0) {    const noun = count > 1 ? 'Videos' : 'Video';    heading = count + ' ' + noun;  }  return (    <section>      <h2>{heading}</h2>      {videos.map(video =>        <Video key={video.id} video={video} />      )}    </section>  );}
```

Example 3 (jsx):
```jsx
import { useState } from 'react';function SearchableVideoList({ videos }) {  const [searchText, setSearchText] = useState('');  const foundVideos = filterVideos(videos, searchText);  return (    <>      <SearchInput        value={searchText}        onChange={newText => setSearchText(newText)} />      <VideoList        videos={foundVideos}        emptyHeading={`No matches for “${searchText}”`} />    </>  );}
```

Example 4 (javascript):
```javascript
import { db } from './database.js';import { Suspense } from 'react';async function ConferencePage({ slug }) {  const conf = await db.Confs.find({ slug });  return (    <ConferenceLayout conf={conf}>      <Suspense fallback={<TalksLoading />}>        <Talks confId={conf.id} />      </Suspense>    </ConferenceLayout>  );}async function Talks({ confId }) {  const talks = await db.Talks.findAll({ confId });  const videos = talks.map(talk => talk.video);  return <SearchableVideoList videos={videos} />;}
```

---

## React Versions

**URL:** https://react.dev/versions

**Contents:**
- React Versions
- Latest version: 19.2
- Previous versions
  - Note
    - Legacy Docs
- Changelog
  - React 19
  - React 18
  - React 17
  - React 16

The React docs at react.dev provide documentation for the latest version of React.

We aim to keep the docs updated within major versions, and do not publish versions for each minor or patch version. When a new major is released, we archive the docs for the previous version as x.react.dev. See our versioning policy for more info.

You can find an archive of previous major versions below.

In 2023, we launched our new docs for React 18 as react.dev. The legacy React 18 docs are available at legacy.reactjs.org. Versions 17 and below are hosted on legacy sites.

For versions older than React 15, see 15.react.dev.

React was open-sourced on May 29, 2013. The initial commit is: 75897c: Initial public release

See the first blog post: Why did we build React?

React was open sourced at Facebook Seattle in 2013:

---
