import { useMemo } from "react";

export const useSortedModels = (models, sort) => {
  const sortedModels = useMemo(() => {
    if (sort) {
      return [...models].sort((a, b) => a[sort].localeCompare(b[sort]));
    }
    return models;
  }, [sort, models]);

  return sortedModels;
};

export const useModels = (models, sort, query) => {
  const sortedModels = useSortedModels(models, sort);

  const sortedAndSearchedModels = useMemo(() => {
    return sortedModels?.filter((model) =>
      model.name.toLowerCase().includes(query.toLowerCase())
    );
  }, [query, sortedModels]);

  return sortedAndSearchedModels;
};
