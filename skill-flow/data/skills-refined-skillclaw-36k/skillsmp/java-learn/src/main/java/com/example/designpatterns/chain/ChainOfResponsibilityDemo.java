package com.example.designpatterns.chain;

import java.util.List;

public class ChainOfResponsibilityDemo {

    public static void main(String[] args) {
        HandlerChain chain = new HandlerChain(java.util.Arrays.asList(
                new AuthHandler(),
                new RiskHandler(),
                new BusinessHandler()
        ));

        System.out.println("=== request ok ===");
        chain.handle(new Request("alice", 100));

        System.out.println("=== request rejected ===");
        try {
            chain.handle(new Request("", 100));
        } catch (RuntimeException e) {
            System.out.println("rejected: " + e.getMessage());
        }
    }

    static class Request {
        private final String userId;
        private final int amount;

        Request(String userId, int amount) {
            this.userId = userId;
            this.amount = amount;
        }

        String getUserId() {
            return userId;
        }

        int getAmount() {
            return amount;
        }
    }

    interface Handler {
        void handle(Request request);
    }

    static class HandlerChain {
        private final List<Handler> handlers;

        HandlerChain(List<Handler> handlers) {
            this.handlers = handlers;
        }

        void handle(Request request) {
            for (Handler handler : handlers) {
                handler.handle(request);
            }
        }
    }

    static class AuthHandler implements Handler {
        @Override
        public void handle(Request request) {
            if (request.getUserId() == null || request.getUserId().trim().isEmpty()) {
                throw new IllegalArgumentException("userId missing");
            }
            System.out.println("auth passed");
        }
    }

    static class RiskHandler implements Handler {
        @Override
        public void handle(Request request) {
            if (request.getAmount() > 1000) {
                throw new IllegalArgumentException("risk too high");
            }
            System.out.println("risk passed");
        }
    }

    static class BusinessHandler implements Handler {
        @Override
        public void handle(Request request) {
            System.out.println("business done for " + request.getUserId());
        }
    }
}
