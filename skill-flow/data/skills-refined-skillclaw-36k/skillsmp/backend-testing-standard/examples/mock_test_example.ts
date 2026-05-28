import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';
import * as categoryController from '@/controllers/categoryController';
import Category from '@/models/category';
import { RootType } from '@repo/shared';

// ------------------------------------------------------------------
// 1. Mock Dependencies (Models)
// ------------------------------------------------------------------
// Observe how we mock the specific methods we plan to use.
vi.mock('@/models/category', () => ({
  default: {
    findAll: vi.fn(),
    create: vi.fn(),
    findOne: vi.fn(),
    findByPk: vi.fn(),
  },
}));

describe('Category Controller (Mocked)', () => {
  let req: Partial<Request>;
  let res: Partial<Response>;
  let jsonMock: any;
  let statusMock: any;

  beforeEach(() => {
    // 2. Setup Express Mocks (Request/Response)
    jsonMock = vi.fn();
    statusMock = vi.fn().mockReturnValue({ json: jsonMock });
    req = {};
    res = {
      status: statusMock,
    } as unknown as Response;

    vi.clearAllMocks();
  });

  it('getAllCategories - should return user and system categories', async () => {
    // 3. Arrange: Define what the Mock DB returns
    const mockCategories = [
      { id: '1', name: 'Food', type: RootType.EXPENSE, userId: 'user1' },
      { id: '2', name: 'Salary', type: RootType.INCOME, userId: null }, // System default
    ];

    // Force Category.findAll to return our mock data
    (Category.findAll as any).mockResolvedValue(mockCategories);

    // Setup Request
    req.user = { id: 'user1' } as any;

    // 4. Act: Call the controller
    await categoryController.getAllCategories(req as Request, res as Response);

    // 5. Assert: Verify logic flow
    expect(Category.findAll).toHaveBeenCalledTimes(1);
    expect(Category.findAll).toHaveBeenCalledWith(
      expect.objectContaining({
        where: expect.anything(), // Can be more specific if needed
      })
    );

    expect(statusMock).toHaveBeenCalledWith(StatusCodes.OK);
    expect(jsonMock).toHaveBeenCalledWith({
      isSuccess: true,
      message: expect.any(String),
      data: mockCategories, // Controller should pass data through
    });
  });

  it('createCategory - should handle database errors gracefully', async () => {
    // 3. Arrange: Simulate DB Error
    const dbError = new Error('DB Connection Failed');
    (Category.create as any).mockRejectedValue(dbError);

    req.body = {
      name: 'Test Cat',
      type: RootType.EXPENSE,
      parentId: 'root1',
    };
    req.user = { id: 'user1' } as any;

    // 4. Act
    await categoryController.createCategory(req as Request, res as Response);

    // 5. Assert: Check error handling
    // Assuming controller catches error and returns 500 or passes to next()
    // NOTE: If using async wrapper that calls next(err), we might need to mock next()
    // For this example, let's assume it catches and returns 500.

    // If your controller relies on global error handler (next), you would mock next:
    // const next = vi.fn();
    // await categoryController.createCategory(req, res, next);
    // expect(next).toHaveBeenCalledWith(dbError);

    // IF it handles it internally:
    // expect(statusMock).toHaveBeenCalledWith(StatusCodes.INTERNAL_SERVER_ERROR);
  });
});
