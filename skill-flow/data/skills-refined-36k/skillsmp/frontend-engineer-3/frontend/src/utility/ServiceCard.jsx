import React from 'react'
import { Card,Button } from "flowbite-react";


const ServiceCard = ({item,index}) => {
  return (
    <Card className="w-full xl:w-1/4">
      <h5 className="mb-2 text-3xl font-bold text-gray-900 dark:text-white text-center">{item.title}</h5>
      <p className="mb-5  text-center text-wrap text-gray-500 dark:text-gray-400 sm:text-lg">
       {item.description}
      </p>
     <Button color='dark'> Choose your Service </Button>
    </Card>
  )
}

export default ServiceCard



