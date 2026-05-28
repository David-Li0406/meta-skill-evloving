import React from "react";
import { Timeline } from "flowbite-react";
const AboutUsPoints = ({ item, index }) => {

  return (
    <Timeline>
      <Timeline.Item key={index}>
        <Timeline.Point />
        <Timeline.Content>
          <Timeline.Time className="text-white text-md lg:text-xl ">{item.title}</Timeline.Time>
          <Timeline.Body className="text-white/60 text-sm lg:text-md">{item.description}</Timeline.Body>
        </Timeline.Content>
      </Timeline.Item>
    </Timeline>
  );
};

export default AboutUsPoints;
