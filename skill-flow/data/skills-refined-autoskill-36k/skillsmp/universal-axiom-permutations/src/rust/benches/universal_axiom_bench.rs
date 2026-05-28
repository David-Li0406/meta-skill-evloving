use criterion::{black_box, criterion_group, criterion_main, Criterion, BenchmarkId};
use universal_axiom::{UniversalAxiom, AxiomSimulator, fibonacci_sequence};


fn benchmark_basic_computation(c: &mut Criterion) {
    let mut group = c.benchmark_group("Basic Computation");

    for n in [1, 10, 20].iter() {
        group.bench_with_input(BenchmarkId::new("n", n), n, |b, &n| {
            b.iter(|| {
                let axiom = UniversalAxiom::with_params(
                    1.0, 1.0, 1.0, 0.0, 1.0, 1.0, black_box(n)
                );
                black_box(axiom.compute_intelligence())
            });
        });
    }

    group.finish();
}


fn benchmark_evolution(c: &mut Criterion) {
    let mut group = c.benchmark_group("Evolution");

    group.bench_function("10_steps", |b| {
        b.iter(|| {
            let mut axiom = UniversalAxiom::with_params(
                1.0, 1.0, 1.0, 0.0, 1.0, 1.0, black_box(1)
            );
            for _ in 0..10 {
                axiom.evolve(black_box(1.0));
            }
        });
    });

    group.bench_function("100_steps", |b| {
        b.iter(|| {
            let mut axiom = UniversalAxiom::with_params(
                1.0, 1.0, 1.0, 0.0, 1.0, 1.0, black_box(1)
            );
            for _ in 0..100 {
                axiom.evolve(black_box(1.0));
            }
        });
    });

    group.finish();
}


fn benchmark_fibonacci_generation(c: &mut Criterion) {
    let mut group = c.benchmark_group("Fibonacci Generation");

    for n in [12, 50].iter() {
        group.bench_with_input(BenchmarkId::new("n", n), n, |b, &n| {
            b.iter(|| {
                black_box(fibonacci_sequence(black_box(n)))
            });
        });
    }

    group.finish();
}


fn benchmark_state_access(c: &mut Criterion) {
    c.bench_function("state_access", |b| {
        let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 10);
        b.iter(|| {
            black_box(axiom.get_state())
        });
    });
}


fn benchmark_contradiction_resolution(c: &mut Criterion) {
    c.bench_function("contradiction_resolution", |b| {
        b.iter(|| {
            let axiom = UniversalAxiom::with_params(1.0, 1.0, 1.0, 0.8, 1.0, 1.0, 5);
            let mut simulator = AxiomSimulator::new(axiom);
            let history = simulator.simulate_contradiction_resolution(black_box(1.5), black_box(5));
            black_box(history.len())
        });
    });
}


criterion_group!(
    benches,
    benchmark_basic_computation,
    benchmark_evolution,
    benchmark_fibonacci_generation,
    benchmark_state_access,
    benchmark_contradiction_resolution
);

criterion_main!(benches);
