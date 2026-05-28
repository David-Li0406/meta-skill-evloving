using Test
using DelimitedFiles

include(joinpath(@__DIR__, "..", "..", "src", "julia", "UniversalAxiom.jl"))
using .UniversalAxiom

@testset "Julia Universal Axiom" begin
    @testset "Foundation Layer" begin
        foundation = FoundationLayer(2.0, 3.0, 1.5)
        @test compute(foundation) == 2.0 * 3.0 * 1.5
    end

    @testset "Dynamic Layer" begin
        dynamic = DynamicLayer(10)
        @test fibonacci(dynamic) == 89
        @test exponential_growth(dynamic) == (2 * (3.0 ^ 10)) - 1
    end

    @testset "Cognitive Layer" begin
        cognitive = CognitiveLayer(0.2, 1.5, 2.0)
        @test compute(cognitive) == 0.8 * 1.5 * 2.0
    end

    @testset "Golden Cases Parity" begin
        golden_path = normpath(joinpath(@__DIR__, "..", "golden_cases.csv"))
        data = readdlm(golden_path, ',', String)
        for row in eachrow(data[2:end, :])
            axiom = Axiom(
                impulses = parse(Float64, row[2]),
                elements = parse(Float64, row[3]),
                pressure = parse(Float64, row[4]),
                subjectivity = parse(Float64, row[5]),
                purpose = parse(Float64, row[6]),
                time = parse(Float64, row[7]),
                n = parse(Int64, row[8])
            )
            expected = parse(Float64, row[9])
            actual = compute_intelligence(axiom)
            @test isapprox(actual, expected; atol=1e-6, rtol=1e-9)
        end
    end
end
