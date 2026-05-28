// ProfileService.ts
// SINGLE RESPONSIBILITY: User profile management (name, email, avatar)
// REASON TO CHANGE: Profile fields or validation rules change

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  avatarUrl?: string;
}

export interface ProfileRepository {
  findById(id: string): Promise<UserProfile | null>;
  update(profile: UserProfile): Promise<void>;
}

export interface AvatarStorage {
  upload(userId: string, file: Buffer): Promise<string>;
  delete(url: string): Promise<void>;
}

export class ProfileService {
  constructor(
    private profileRepository: ProfileRepository,
    private avatarStorage: AvatarStorage
  ) {}

  async getProfile(userId: string): Promise<UserProfile | null> {
    return this.profileRepository.findById(userId);
  }

  async updateName(userId: string, name: string): Promise<boolean> {
    const profile = await this.profileRepository.findById(userId);
    if (!profile) return false;

    profile.name = name;
    await this.profileRepository.update(profile);
    return true;
  }

  async updateEmail(userId: string, email: string): Promise<boolean> {
    const profile = await this.profileRepository.findById(userId);
    if (!profile) return false;

    profile.email = email;
    await this.profileRepository.update(profile);
    return true;
  }

  async updateAvatar(userId: string, file: Buffer): Promise<string | null> {
    const profile = await this.profileRepository.findById(userId);
    if (!profile) return null;

    if (profile.avatarUrl) {
      await this.avatarStorage.delete(profile.avatarUrl);
    }

    const newUrl = await this.avatarStorage.upload(userId, file);
    profile.avatarUrl = newUrl;
    await this.profileRepository.update(profile);
    return newUrl;
  }
}
