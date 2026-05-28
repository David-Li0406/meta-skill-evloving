// AuthenticationService.ts
// SINGLE RESPONSIBILITY: User authentication (login, logout, password reset)
// REASON TO CHANGE: Authentication logic or security requirements change

export interface AuthResult {
  success: boolean;
  token?: string;
  error?: string;
}

export interface User {
  id: string;
  email: string;
  passwordHash: string;
}

export interface TokenService {
  generate(userId: string): string;
  invalidate(token: string): void;
}

export interface PasswordHasher {
  hash(password: string): Promise<string>;
  verify(password: string, hash: string): Promise<boolean>;
}

export interface UserRepository {
  findByEmail(email: string): Promise<User | null>;
  findById(id: string): Promise<User | null>;
  updatePassword(userId: string, passwordHash: string): Promise<void>;
}

export class AuthenticationService {
  constructor(
    private userRepository: UserRepository,
    private tokenService: TokenService,
    private passwordHasher: PasswordHasher
  ) {}

  async login(email: string, password: string): Promise<AuthResult> {
    const user = await this.userRepository.findByEmail(email);
    if (!user) {
      return { success: false, error: 'Invalid credentials' };
    }

    const valid = await this.passwordHasher.verify(password, user.passwordHash);
    if (!valid) {
      return { success: false, error: 'Invalid credentials' };
    }

    const token = this.tokenService.generate(user.id);
    return { success: true, token };
  }

  logout(token: string): void {
    this.tokenService.invalidate(token);
  }

  async resetPassword(userId: string, newPassword: string): Promise<boolean> {
    const user = await this.userRepository.findById(userId);
    if (!user) return false;

    const hash = await this.passwordHasher.hash(newPassword);
    await this.userRepository.updatePassword(userId, hash);
    return true;
  }
}
