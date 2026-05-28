import { useState, useCallback, useMemo } from 'react';
import { UniversalAxiom, AxiomState, getCoherenceMetric } from '../core/axiom';

export interface AxiomParams {
    impulses: number;
    elements: number;
    pressure: number;
    subjectivity: number;
    purpose: number;
    time: number;
    n: number;
}

const DEFAULT_PARAMS: AxiomParams = {
    impulses: 5.0,
    elements: 3.0,
    pressure: 1.0,
    subjectivity: 0.2,
    purpose: 0.9,
    time: 1.0,
    n: 5
};

export function useAxiom(initialParams: Partial<AxiomParams> = {}) {
    const [params, setParams] = useState<AxiomParams>({
        ...DEFAULT_PARAMS,
        ...initialParams
    });

    const axiom = useMemo(() => {
        return new UniversalAxiom(params);
    }, [params]);

    const state = useMemo<AxiomState>(() => {
        return axiom.getState();
    }, [axiom]);

    const coherence = useMemo(() => {
        return getCoherenceMetric(state);
    }, [state]);

    const setParam = useCallback(<K extends keyof AxiomParams>(
        key: K,
        value: AxiomParams[K]
    ) => {
        setParams(prev => ({ ...prev, [key]: value }));
    }, []);

    const resetParams = useCallback(() => {
        setParams(DEFAULT_PARAMS);
    }, []);

    return {
        params,
        state,
        coherence,
        setParam,
        setParams,
        resetParams
    };
}
