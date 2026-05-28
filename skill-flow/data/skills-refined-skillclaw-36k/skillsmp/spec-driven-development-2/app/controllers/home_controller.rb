class HomeController < ApplicationController
  def index
    @promise_fitness_kits = PromiseFitnessKit.ordered_by_name
  end
end
