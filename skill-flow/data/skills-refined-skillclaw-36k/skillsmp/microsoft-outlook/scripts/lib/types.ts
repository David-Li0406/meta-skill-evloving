// Microsoft Graph API Types

export interface MicrosoftUser {
  id: string;
  displayName: string;
  surname: string;
  givenName: string;
  userPrincipalName: string;
  mail?: string;
  jobTitle?: string;
  mobilePhone?: string;
  officeLocation?: string;
  preferredLanguage?: string;
}

export interface EmailAddress {
  name: string;
  address: string;
}

export interface Recipient {
  emailAddress: EmailAddress;
}

export interface Message {
  id: string;
  createdDateTime: string;
  lastModifiedDateTime: string;
  changeKey: string;
  categories: string[];
  receivedDateTime: string;
  sentDateTime: string;
  hasAttachments: boolean;
  internetMessageId: string;
  subject: string;
  bodyPreview: string;
  importance: "low" | "normal" | "high";
  parentFolderId: string;
  conversationId: string;
  isDeliveryReceiptRequested: boolean | null;
  isReadReceiptRequested: boolean;
  isRead: boolean;
  isDraft: boolean;
  webLink: string;
  inferenceClassification: "focused" | "other";
  body: {
    contentType: "text" | "html";
    content: string;
  };
  sender: Recipient;
  from: Recipient;
  toRecipients: Recipient[];
  ccRecipients: Recipient[];
  bccRecipients: Recipient[];
  replyTo: Recipient[];
  flag: {
    flagStatus: "notFlagged" | "complete" | "flagged";
  };
}

export interface MessageListResponse {
  "@odata.context": string;
  "@odata.nextLink"?: string;
  value: Message[];
}
