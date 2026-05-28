import { s } from '@hashbrownai/core'

export const userProfileSchema = s.object('User Profile', {
  name: s.string('The full name of the user'),
  email: s.string('The email address of the user'),
  age: s.anyOf([s.number('The age of the user'), s.nullish()]),
})
